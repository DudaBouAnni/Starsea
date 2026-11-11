from datetime import timedelta

import pytest
from sqlalchemy import create_engine, inspect, text

from app.database.migrate_nearby import migrate
from app.models import Event, Notification
from app.services.geo_service import distance_km, local_today


def create_show(client, **changes):
    payload = {
        "event_name": "Show perto",
        "event_description": "Música ao vivo",
        "event_date": str(local_today() + timedelta(days=1)),
        "event_location": "São Paulo",
        "ticket_link": "https://example.test/ingressos",
        "organizer_id": 1,
        "latitude": -23.551,
        "longitude": -46.634,
    }
    payload.update(changes)
    response = client.post("/events/", json=payload)
    assert response.status_code == 200, response.text
    return response.json()


def locate(client, latitude=-23.5505, longitude=-46.6333):
    response = client.put("/users/1/location", json={"latitude": latitude, "longitude": longitude})
    assert response.status_code == 200, response.text


def test_notifications_created_automatically_and_not_duplicated(client, db):
    locate(client)
    show = create_show(client)
    notices = client.get("/users/1/notifications").json()
    assert len(notices) == 1
    assert notices[0]["event_id"] == show["event_id"]
    assert notices[0]["distance_km"] < 1
    assert client.get("/users/2/notifications").json() == []
    assert client.post("/users/1/notifications/refresh").json() == {"created": 0}
    assert db.query(Notification).count() == 1
    notice_id = notices[0]["notification_id"]
    assert client.patch(f"/users/2/notifications/{notice_id}/read").status_code == 404
    assert client.patch(f"/users/1/notifications/{notice_id}/read").json()["is_read"] is True
    client.post("/users/1/notifications/refresh")
    assert client.get("/users/1/notifications?unread_only=true").json() == []


def test_existing_shows_location_preferences_and_opt_out(client):
    create_show(client)
    assert client.get("/users/1/nearby-events").status_code == 400
    locate(client)
    assert len(client.get("/users/1/notifications").json()) == 1
    response = client.patch(
        "/users/1/notification-preferences", json={"notification_radius_km": 0.001}
    )
    assert response.status_code == 200
    assert client.get("/users/1/notifications").json() == []
    assert client.get("/users/1/nearby-events").json() == []
    assert len(client.get("/users/1/nearby-events?radius_km=50").json()) == 1
    client.patch("/users/1/notification-preferences", json={"notification_radius_km": 50})
    assert len(client.get("/users/1/notifications").json()) == 1
    client.patch("/users/1/notification-preferences", json={"nearby_notifications_enabled": False})
    assert client.get("/users/1/notifications").json() == []
    client.patch("/users/1/notification-preferences", json={"nearby_notifications_enabled": True})
    assert len(client.get("/users/1/notifications").json()) == 1
    assert client.delete("/users/1/location").status_code == 200
    assert client.get("/users/1/notifications").json() == []


def test_nearby_filters_and_sorts_and_does_not_call_google(client, monkeypatch):
    def unexpected(*args, **kwargs):
        pytest.fail("A busca de proximidade deve funcionar sem consultar serviços externos.")

    monkeypatch.setattr("requests.request", unexpected)
    locate(client, 0, 0)
    farther = create_show(client, event_name="Mais distante", latitude=0, longitude=0.2)
    closer = create_show(client, event_name="Mais perto", latitude=0, longitude=0.1)
    create_show(client, event_name="Longe", latitude=40, longitude=40)
    create_show(client, event_name="Sem coordenadas", latitude=None, longitude=None)
    events = client.get("/users/1/nearby-events").json()
    assert [item["event"]["event_id"] for item in events] == [
        closer["event_id"],
        farther["event_id"],
    ]
    assert events[0]["distance_type"] == "straight_line"
    assert len(client.get("/users/1/nearby-events?offset=1&limit=1").json()) == 1
    assert distance_km(0, 0, 0, 0) == 0
    assert distance_km(0, 0, 0, 1) == pytest.approx(111.195, abs=0.01)
    assert distance_km(0, 0, 0, 180) == pytest.approx(20015.114, abs=0.01)


def test_event_changes_reconcile_notices_and_delete_cascades(client, db):
    locate(client)
    show = create_show(client)
    event_id = show["event_id"]
    result = client.patch(
        f"/events/{event_id}", json={"event_name": "Outro nome", "latitude": 0, "longitude": 0}
    )
    assert result.status_code == 200
    db.expire_all()
    assert db.get(Event, event_id).event_name == "Outro nome"
    assert db.get(Event, event_id).latitude == 0
    assert client.get("/users/1/notifications").json() == []
    client.patch(f"/events/{event_id}", json={"latitude": -23.551, "longitude": -46.634})
    assert len(client.get("/users/1/notifications").json()) == 1
    assert client.delete(f"/events/{event_id}").status_code == 200
    assert db.query(Notification).count() == 0


def test_expired_show_not_visible(client, db):
    locate(client)
    show = create_show(client)
    db.get(Event, show["event_id"]).event_date = local_today() - timedelta(days=1)
    db.commit()
    assert client.get("/users/1/notifications").json() == []
    assert client.get("/users/1/nearby-events").json() == []


def test_transaction_does_not_leave_partial_event_or_notices(client, db):
    locate(client)
    payload = {
        "event_name": "Inválido",
        "event_description": "teste",
        "event_date": str(local_today()),
        "ticket_link": "https://example.test",
        "event_location": "SP",
        "organizer_id": 1,
        "artists": ["Inexistente"],
        "latitude": -23.551,
        "longitude": -46.634,
    }
    assert client.post("/events/", json=payload).status_code == 404
    assert db.query(Event).count() == 0
    assert db.query(Notification).count() == 0


@pytest.mark.parametrize(
    "payload",
    [
        {"latitude": 91, "longitude": 0},
        {"latitude": 0, "longitude": -181},
        {"latitude": None, "longitude": 0},
        {"latitude": 0},
    ],
)
def test_location_validation(client, payload):
    assert client.put("/users/1/location", json=payload).status_code == 422


def test_preferences_and_coordinate_pair_validation(client):
    assert (
        client.put("/users/999/location", json={"latitude": 0, "longitude": 0}).status_code == 404
    )
    for payload in [
        {"notification_radius_km": 0},
        {"notification_radius_km": 1001},
        {"notification_radius_km": None},
        {"nearby_notifications_enabled": None},
    ]:
        assert client.patch("/users/1/notification-preferences", json=payload).status_code == 422
    show = create_show(client)
    assert client.patch(f"/events/{show['event_id']}", json={"latitude": 10}).status_code == 422
    assert (
        client.patch(
            f"/events/{show['event_id']}", json={"latitude": None, "longitude": None}
        ).status_code
        == 200
    )


def test_user_delete_cascades_notifications(client, db):
    locate(client)
    create_show(client)
    assert client.delete("/users/1").status_code == 200
    assert db.query(Notification).count() == 0


def test_repeatable_migration_preserves_old_rows():
    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE users (user_id INTEGER PRIMARY KEY, username VARCHAR(100))")
        )
        connection.execute(text("INSERT INTO users VALUES (1, 'Ana')"))
        connection.execute(text("CREATE TABLE events (event_id INTEGER PRIMARY KEY)"))
        migrate(connection)
        migrate(connection)
        row = connection.execute(
            text("SELECT username, notification_radius_km, nearby_notifications_enabled FROM users")
        ).one()
        assert tuple(row) == ("Ana", 50, 1)
        assert "notifications" in inspect(connection).get_table_names()
        assert {"latitude", "longitude"} <= {
            column["name"] for column in inspect(connection).get_columns("events")
        }
    engine.dispose()
