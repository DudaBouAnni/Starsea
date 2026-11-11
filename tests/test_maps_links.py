from urllib.parse import parse_qs, urlparse

import pytest

from app.models import Event
from app.services.geo_service import local_today


def save_event(db, **values):
    event = Event(
        event_name="Show",
        event_description="Música ao vivo",
        event_date=local_today(),
        ticket_link="https://example.test/ingressos",
        organizer_id=1,
        event_location=values.pop("event_location", "Praça da Sé, São Paulo"),
        **values,
    )
    db.add(event)
    db.commit()
    return event


@pytest.mark.parametrize(
    "coordinates, expected",
    [
        ({"latitude": -23.5505, "longitude": -46.6333}, "-23.5505,-46.6333"),
        ({"latitude": 0, "longitude": 0}, "0.0,0.0"),
        ({}, "Praça da Sé, São Paulo"),
    ],
)
def test_open_maps_at_event_without_user_location_or_key(
    client, db, monkeypatch, coordinates, expected
):

    def unexpected(*args, **kwargs):
        pytest.fail("Abrir o local não deve consultar uma API externa.")

    monkeypatch.setattr("requests.request", unexpected)
    event = save_event(db, **coordinates)
    response = client.get(f"/events/{event.event_id}/map", follow_redirects=False)
    assert response.status_code == 307
    url = urlparse(response.headers["location"])
    assert url.scheme == "https"
    assert url.netloc == "www.google.com"
    assert url.path == "/maps/search/"
    query = parse_qs(url.query)
    assert query == {"api": ["1"], "query": [expected]}


def test_event_cards_expose_same_maps_location_link(client, db):
    event = save_event(db, latitude=-23.5505, longitude=-46.6333)
    cards = client.get("/events/").json()
    assert (
        cards[0]["maps_url"]
        == client.get(f"/events/{event.event_id}/map", follow_redirects=False).headers["location"]
    )
    client.put("/users/1/location", json={"latitude": -23.5505, "longitude": -46.6333})
    nearby = client.get("/users/1/nearby-events").json()
    assert nearby[0]["maps_url"] == cards[0]["maps_url"]
    assert nearby[0]["event"]["maps_url"] == cards[0]["maps_url"]


def test_address_is_encoded_and_cannot_change_maps_domain(client, db):
    event = save_event(db, event_location="Casa A & B, Rua São João, 50 #Centro")
    response = client.get(f"/events/{event.event_id}/map", follow_redirects=False)
    query = parse_qs(urlparse(response.headers["location"]).query)
    assert query["query"] == [event.event_location]
    assert set(query) == {"api", "query"}


def test_maps_missing_location_or_event(client, db):
    event = save_event(db, event_location=" ")
    assert client.get(f"/events/{event.event_id}/map", follow_redirects=False).status_code == 400
    assert client.get("/events/999/map", follow_redirects=False).status_code == 404
    assert client.get("/events/").json()[0]["maps_url"] is None
