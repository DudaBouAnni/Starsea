from datetime import timedelta
from urllib.parse import parse_qs, urlparse

import pytest
import requests
from sqlalchemy import create_engine, inspect, text

from app.database.migrate_music import migrate
from app.models import Artist, Event, Genre, MusicPreference, Notification, User
from app.services.geo_service import local_today
from app.services.music_service import import_spotify_artists


def artist(db, name="Artista favorito", spotify_id=None):
    item = Artist(artist_name=name, spotify_id=spotify_id)
    db.add(item)
    db.commit()
    return item


def show(client, name, artists=None, latitude=-23.551, longitude=-46.634):
    response = client.post(
        "/events/",
        json={
            "event_name": name,
            "event_description": "Show ao vivo",
            "event_date": str(local_today() + timedelta(days=1)),
            "ticket_link": "https://example.test",
            "event_location": "SP",
            "organizer_id": 1,
            "artists": artists or [],
            "latitude": latitude,
            "longitude": longitude,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()["event_id"]


def locate(client):
    assert (
        client.put(
            "/users/1/location", json={"latitude": -23.5505, "longitude": -46.6333}
        ).status_code
        == 200
    )


def authorized_callback(client):
    login = client.get("/auth/login")
    assert login.status_code == 200, login.text
    params = parse_qs(urlparse(login.json()["login_url"]).query)
    assert "user-top-read" in params["scope"][0].split()
    cookie = login.headers["set-cookie"]
    assert "HttpOnly" in cookie and "Max-Age=600" in cookie and "SameSite=lax" in cookie
    return client.get("/auth/callback", params={"code": "test-code", "state": params["state"][0]})


def mock_spotify(monkeypatch, top_items=None, failure=None):
    calls = []

    class Response:
        status_code = 200
        headers = {}

        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            pass

        def json(self):
            return self.payload

    def request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        assert kwargs["timeout"] == (3.05, 10)
        if url.endswith("/api/token"):
            return Response(
                {
                    "access_token": "never-return-this-token",
                    "refresh_token": "never-store-this-token",
                }
            )
        assert kwargs["headers"]["Authorization"] == "Bearer never-return-this-token"
        if url.endswith("/me/top/artists"):
            if failure:
                raise failure
            assert kwargs["params"] == {"time_range": "medium_term", "limit": 50}
            return Response(
                {
                    "items": top_items
                    if top_items is not None
                    else [{"id": "spotifyFavorite", "name": "Artista favorito"}]
                }
            )
        return Response(
            {
                "id": "spotifyUser",
                "email": "ana@example.test",
                "display_name": "Ana",
                "country": "BR",
                "images": [],
            }
        )

    monkeypatch.setattr("app.services.spotify_service.requests.request", request)
    return calls


def test_spotify_import_matches_show_and_returns_only_public_fields(client, db, monkeypatch):
    favorite = artist(db)
    locate(client)
    favorite_event = show(client, "Show favorito", [favorite.artist_name])
    show(client, "Sem artista preferido")
    db.get(User, 1).user_password = "local-password-must-stay-private"
    db.commit()
    calls = mock_spotify(monkeypatch)
    response = authorized_callback(client)
    assert response.status_code == 200, response.text
    assert response.json()["imported_artists"] == 1
    assert response.json()["user"]["user_id"] == 1
    assert "user_password" not in response.text
    assert "never-return-this-token" not in response.text
    assert "local-password-must-stay-private" not in response.text
    assert "no-store" in response.headers["cache-control"]
    profile = client.get("/users/1/music-profile").json()
    assert profile["personalized_notifications_only"] is True
    assert profile["artists"][0]["artist_id"] == favorite.artist_id
    assert profile["artists"][0]["spotify_url"].endswith("/spotifyFavorite")
    assert len(calls) == 3
    notices = client.get("/users/1/notifications").json()
    assert [item["event_id"] for item in notices] == [favorite_event]
    assert favorite.artist_name in notices[0]["message"]
    assert (
        client.get("/users/1/recommended-events").json()[0]["event"]["event_id"] == favorite_event
    )
    assert len(client.get("/users/1/nearby-events").json()) == 2


def test_manual_preferences_drive_creation_and_lineup_changes(client, db):
    favorite = artist(db)
    other = artist(db, "Outro artista")
    locate(client)
    assert client.put(f"/users/1/music-profile/artists/{favorite.artist_id}").status_code == 200
    favorite_event = show(client, "Favorito", [favorite.artist_name])
    other_event = show(client, "Outro", [other.artist_name])
    show(client, "Favorito longe", [favorite.artist_name], latitude=40, longitude=40)
    assert [item["event_id"] for item in client.get("/users/1/notifications").json()] == [
        favorite_event
    ]
    assert client.post(f"/events/{other_event}/artists/{favorite.artist_id}").status_code == 200
    assert len(client.get("/users/1/notifications").json()) == 2
    assert (
        client.delete(f"/events/{favorite_event}/artists/{favorite.artist_id}").status_code == 200
    )
    assert [item["event_id"] for item in client.get("/users/1/notifications").json()] == [
        other_event
    ]
    assert client.put(f"/users/1/music-profile/artists/{favorite.artist_id}").status_code == 200
    assert db.query(MusicPreference).count() == 1
    assert client.delete(f"/users/1/music-profile/artists/{favorite.artist_id}").status_code == 200
    assert client.get("/users/1/notifications").json() == []


def test_snapshot_replacement_preserves_manual_choices(client, db):
    manual = artist(db, "Escolha manual")
    client.put(f"/users/1/music-profile/artists/{manual.artist_id}")
    user = db.get(User, 1)
    import_spotify_artists(user, [{"id": "old", "name": "Antigo"}], db)
    db.commit()
    import_spotify_artists(user, [{"id": "new", "name": "Novo"}, {"id": "new", "name": "Novo"}], db)
    db.commit()
    assert {(item.source, item.artist.artist_name) for item in user.music_preferences} == {
        ("manual", "Escolha manual"),
        ("spotify", "Novo"),
    }
    client.delete("/users/1/music-profile/spotify")
    profile = client.get("/users/1/music-profile").json()
    assert profile["personalized_notifications_only"] is True
    assert [item["source"] for item in profile["artists"]] == ["manual"]


def test_no_false_positive_for_ambiguous_names_or_conflicting_spotify_ids(client, db):
    first = artist(db, "Mesmo nome")
    artist(db, "Mesmo nome")
    old_id = artist(db, "Nome diferente", "oldProviderId")
    locate(client)
    event_id = show(client, "Show ambíguo", [first.artist_name, old_id.artist_name])
    import_spotify_artists(
        db.get(User, 1),
        [
            {"id": "newProviderId", "name": "Mesmo nome"},
            {"id": "anotherProviderId", "name": "Nome diferente"},
        ],
        db,
    )
    db.commit()
    assert client.get("/users/1/recommended-events").json() == []
    assert client.get("/users/1/notifications").json() == []
    assert db.get(Artist, first.artist_id).spotify_id is None
    assert db.get(Artist, old_id.artist_id).spotify_id == "oldProviderId"


def test_normalized_unique_name_and_stable_provider_id(db):
    local = artist(db, "  THE   BAND ")
    user = db.get(User, 1)
    import_spotify_artists(user, [{"id": "stableId", "name": "The Band"}], db)
    db.commit()
    assert user.music_preferences[0].artist_id == local.artist_id
    import_spotify_artists(user, [{"id": "stableId", "name": "Novo nome artístico"}], db)
    db.commit()
    assert user.music_preferences[0].artist_id == local.artist_id
    assert db.query(Artist).count() == 1


def test_empty_taste_does_not_fall_back_to_every_show(client, db):
    locate(client)
    show(client, "Geral")
    import_spotify_artists(db.get(User, 1), [], db)
    db.commit()
    assert client.get("/users/1/notifications").json() == []
    assert client.get("/users/1/recommended-events").json() == []
    client.patch(
        "/users/1/notification-preferences", json={"personalized_notifications_only": False}
    )
    assert len(client.get("/users/1/notifications").json()) == 1
    assert client.get("/users/1/recommended-events").json() == []


def test_reimport_preserves_explicit_general_notification_preference(client, db):
    user = db.get(User, 1)
    import_spotify_artists(user, [{"id": "valid", "name": "Favorito"}], db)
    db.commit()
    assert user.spotify_preferences_synced_at is not None
    client.patch(
        "/users/1/notification-preferences", json={"personalized_notifications_only": False}
    )
    import_spotify_artists(user, [{"id": "valid", "name": "Favorito"}], db)
    db.commit()
    assert user.personalized_notifications_only is False


def test_failed_import_preserves_previous_profile(client, db, monkeypatch):
    user = db.get(User, 1)
    import_spotify_artists(user, [{"id": "valid", "name": "Preferido"}], db)
    db.commit()
    mock_spotify(monkeypatch, top_items=[{"id": "bad", "name": None}])
    response = authorized_callback(client)
    assert response.status_code == 502
    db.expire_all()
    assert [(item.artist.spotify_id, item.source) for item in user.music_preferences] == [
        ("valid", "spotify")
    ]
    assert user.spotify_id is None


def test_late_import_failure_rolls_back_deleted_preferences(client, db, monkeypatch):
    user = db.get(User, 1)
    import_spotify_artists(user, [{"id": "valid", "name": "Preferido"}], db)
    db.commit()
    mock_spotify(monkeypatch)

    def fail_resolution(*args):
        raise RuntimeError("Simulated storage error")

    monkeypatch.setattr("app.services.music_service._resolve_spotify_artist", fail_resolution)
    with pytest.raises(RuntimeError):
        authorized_callback(client)
    assert db.query(MusicPreference).one().artist.spotify_id == "valid"
    assert db.get(User, 1).spotify_id is None


def test_oauth_state_and_denial(client, monkeypatch):
    assert client.get("/auth/callback?code=x").status_code == 400
    response = client.get("/auth/login")
    params = parse_qs(urlparse(response.json()["login_url"]).query)
    assert client.get("/auth/callback?code=x&state=wrong").status_code == 400
    assert (
        client.get("/auth/callback", params={"code": "x", "state": "estado-inválido"}).status_code
        == 400
    )
    assert (
        client.get(
            "/auth/callback", params={"state": params["state"][0], "error": "access_denied"}
        ).status_code
        == 400
    )
    mock_spotify(monkeypatch)
    assert authorized_callback(client).status_code == 200
    assert (
        client.get("/auth/callback", params={"code": "x", "state": params["state"][0]}).status_code
        == 400
    )


@pytest.mark.parametrize("status", [401, 403, 429])
def test_provider_denial_and_rate_limit(client, monkeypatch, status):
    class Response:
        status_code = status
        headers = {"Retry-After": "120"}

    monkeypatch.setattr(
        "app.services.spotify_service.requests.request", lambda *args, **kwargs: Response()
    )
    response = authorized_callback(client)
    assert response.status_code == status
    if status == 429:
        assert response.headers["retry-after"] == "120"


def test_timeout_and_no_credentials(client, db, monkeypatch):
    mock_spotify(monkeypatch, failure=requests.Timeout())
    assert authorized_callback(client).status_code == 504
    assert db.query(MusicPreference).count() == 0
    monkeypatch.setattr("app.core.settings.settings.SPOTIFY_CLIENT_ID", "")
    assert client.get("/auth/login").status_code == 503


def test_artist_spotify_id_registration_and_validation(client, db):
    first = client.post("/artists/", json={"artist_name": "Primeiro", "spotify_id": "providerId"})
    assert first.status_code == 200
    assert first.json()["spotify_id"] == "providerId"
    assert (
        client.post(
            "/artists/", json={"artist_name": "Duplicado", "spotify_id": "providerId"}
        ).status_code
        == 409
    )
    assert (
        client.post(
            "/artists/", json={"artist_name": "Inválido", "spotify_id": "bad id"}
        ).status_code
        == 422
    )
    assert len(client.get("/artists/").json()) == 1
    assert client.put("/users/999/music-profile/artists/1").status_code == 404
    assert client.put("/users/1/music-profile/artists/999").status_code == 404


def test_music_migration_is_repeatable_and_preserves_existing_data():
    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE users (user_id INTEGER PRIMARY KEY, username VARCHAR(100))")
        )
        connection.execute(text("INSERT INTO users VALUES (1, 'Ana')"))
        connection.execute(
            text("CREATE TABLE artists (artist_id INTEGER PRIMARY KEY, artist_name VARCHAR(255))")
        )
        connection.execute(text("INSERT INTO artists VALUES (1, 'Artista')"))
        migrate(connection)
        migrate(connection)
        assert connection.execute(
            text("SELECT username, personalized_notifications_only FROM users")
        ).one() == ("Ana", 0)
        assert connection.execute(text("SELECT artist_name, spotify_id FROM artists")).one() == (
            "Artista",
            None,
        )
        assert "music_preferences" in inspect(connection).get_table_names()
        assert {"artist_spotify_genre", "music_preference_genre"} <= set(
            inspect(connection).get_table_names()
        )
    engine.dispose()


def test_genre_affinity_weights_and_normalizes_provider_tags(client, db):
    user = db.get(User, 1)
    import_spotify_artists(
        user,
        [
            {"id": "a", "name": "A", "genres": ["Rock", " rock ", "POP"]},
            {"id": "b", "name": "B", "genres": ["rock"]},
            {"id": "c", "name": "C", "genres": []},
        ],
        db,
    )
    db.commit()
    profile = client.get("/users/1/music-profile").json()
    assert profile["genre_data_status"] == "partial"
    assert profile["genre_estimation_method"] == "artist_affinity_weighted"
    rock, pop = profile["genres"]
    assert (rock["genre_name"], pop["genre_name"]) == ("rock", "pop")
    assert rock["score"] == 1
    assert pop["score"] == 0.5
    assert rock["affinity_percent"] == 66.67
    assert rock["artist_count"] == 2
    assert rock["sources"] == ["spotify"]
    assert db.query(Genre).count() == 2


def test_genre_recommends_another_artist_and_explains_the_notification(client, db):
    response = client.post("/genres/", json={"genre_name": "Rock"})
    assert response.status_code == 200, response.text
    rock_id = response.json()["genre_id"]
    other = artist(db, "Outra banda")
    assert client.post(f"/artists/{other.artist_id}/genres/{rock_id}").status_code == 200
    locate(client)
    event_id = show(client, "Nova descoberta", [other.artist_name])
    show(client, "Sem relação")
    import_spotify_artists(
        db.get(User, 1), [{"id": "favorite", "name": "Favorita", "genres": ["rock"]}], db
    )
    db.commit()
    events = client.get("/users/1/recommended-events").json()
    assert [item["event"]["event_id"] for item in events] == [event_id]
    assert events[0]["matched_artists"] == []
    assert events[0]["matched_genres"] == ["Rock"]
    assert events[0]["match_reasons"] == ["genre"]
    notifications = client.get("/users/1/notifications?limit=1").json()
    assert len(notifications) == 1
    assert notifications[0]["event_id"] == event_id
    assert "Porque você gosta de Rock" in notifications[0]["message"]


def test_manual_genres_survive_provider_import_and_source_removal(client, db):
    genre_id = client.post("/genres/", json={"genre_name": "Sertanejo"}).json()["genre_id"]
    for _ in range(2):
        assert client.put(f"/users/1/music-profile/genres/{genre_id}").status_code == 200
    import_spotify_artists(
        db.get(User, 1), [{"id": "rock", "name": "Banda", "genres": ["rock"]}], db
    )
    db.commit()
    profile = client.delete("/users/1/music-profile/spotify").json()
    assert [(genre["genre_name"], genre["sources"]) for genre in profile["genres"]] == [
        ("Sertanejo", ["manual"])
    ]
    assert profile["genre_data_status"] == "manual"
    assert len(db.get(User, 1).genres) == 1
    assert client.delete(f"/users/1/music-profile/genres/{genre_id}").json()["genres"] == []


@pytest.mark.parametrize("metadata", [{}, {"genres": None}, {"genres": []}])
def test_missing_provider_genres_keeps_exact_artist_matches(client, db, metadata):
    favorite = artist(db)
    locate(client)
    event_id = show(client, "Favorito sem gênero", [favorite.artist_name])
    import_spotify_artists(
        db.get(User, 1), [{"id": "favorite", "name": favorite.artist_name, **metadata}], db
    )
    db.commit()
    profile = client.get("/users/1/music-profile").json()
    assert profile["genres"] == []
    assert profile["genre_data_status"] == "unavailable"
    data = client.get("/users/1/recommended-events").json()
    assert data[0]["event"]["event_id"] == event_id
    assert data[0]["match_reasons"] == ["artist"]
    assert data[0]["matched_genres"] == []


def test_provider_genre_updates_preserve_catalog_and_other_user_snapshot(client, db):
    manual = Genre(genre_name="jazz")
    favorite = artist(db)
    favorite.genres.append(manual)
    db.commit()
    ana, bia = db.get(User, 1), db.get(User, 2)
    import_spotify_artists(
        ana, [{"id": "favorite", "name": favorite.artist_name, "genres": ["rock"]}], db
    )
    db.commit()
    import_spotify_artists(
        bia, [{"id": "favorite", "name": favorite.artist_name, "genres": ["pop"]}], db
    )
    db.commit()
    assert client.get("/users/1/music-profile").json()["genres"][0]["genre_name"] == "rock"
    assert client.get("/users/2/music-profile").json()["genres"][0]["genre_name"] == "pop"
    assert [genre.genre_name for genre in favorite.genres] == ["jazz"]
    import_spotify_artists(
        ana, [{"id": "favorite", "name": favorite.artist_name, "genres": []}], db
    )
    db.commit()
    ana_profile = client.get("/users/1/music-profile").json()
    assert ana_profile["genres"][0]["genre_name"] == "jazz"
    assert ana_profile["genres"][0]["sources"] == ["artist_catalog"]
    assert client.get("/users/2/music-profile").json()["genres"][0]["genre_name"] == "pop"
    assert favorite.spotify_genres == []


def test_catalog_changes_refresh_existing_genre_notifications(client, db):
    genre_id = client.post("/genres/", json={"genre_name": "rock"}).json()["genre_id"]
    other = artist(db, "Outra banda")
    locate(client)
    client.put(f"/users/1/music-profile/genres/{genre_id}")
    show(client, "Show", [other.artist_name])
    assert client.get("/users/1/notifications").json() == []
    assert client.post(f"/artists/{other.artist_id}/genres/{genre_id}").status_code == 200
    notice = client.get("/users/1/notifications").json()[0]
    client.patch(f"/users/1/notifications/{notice['notification_id']}/read")
    client.post("/users/1/notifications/refresh")
    assert client.get("/users/1/notifications").json()[0]["is_read"] is True
    assert client.delete(f"/artists/{other.artist_id}/genres/{genre_id}").status_code == 200
    assert client.get("/users/1/notifications").json() == []


def test_genre_deletion_removes_snapshot_references_and_notices(client, db):
    genre_id = client.post("/genres/", json={"genre_name": "rock"}).json()["genre_id"]
    favorite = artist(db)
    favorite.genres.append(db.get(Genre, genre_id))
    db.commit()
    locate(client)
    client.put(f"/users/1/music-profile/genres/{genre_id}")
    show(client, "Show", [favorite.artist_name])
    import_spotify_artists(
        db.get(User, 2), [{"id": "favorite", "name": favorite.artist_name, "genres": ["rock"]}], db
    )
    db.commit()
    assert client.delete(f"/genres/{genre_id}").status_code == 200
    assert client.get("/users/1/notifications").json() == []
    assert client.get("/users/2/music-profile").json()["genres"] == []


def test_genre_weight_counts_an_artist_once_and_limits_inferred_genres(client, db):
    user = db.get(User, 1)
    import_spotify_artists(
        user,
        [
            {"id": f"id{index}", "name": f"Artista {index}", "genres": [f"g{index}"]}
            for index in range(1, 8)
        ],
        db,
    )
    db.commit()
    first = user.music_preferences[0].artist
    profile = client.put(f"/users/1/music-profile/artists/{first.artist_id}").json()
    assert profile["genres"][0]["score"] == 1
    assert sum(item["used_for_recommendations"] for item in profile["genres"]) == 5
    last_id = next(item["genre_id"] for item in profile["genres"] if item["genre_name"] == "g7")
    profile = client.put(f"/users/1/music-profile/genres/{last_id}").json()
    assert (
        next(item for item in profile["genres"] if item["genre_id"] == last_id)[
            "used_for_recommendations"
        ]
        is True
    )


def test_invalid_genre_payload_preserves_previous_import(client, db, monkeypatch):
    user = db.get(User, 1)
    import_spotify_artists(user, [{"id": "valid", "name": "Banda", "genres": ["rock"]}], db)
    db.commit()
    mock_spotify(monkeypatch, top_items=[{"id": "valid", "name": "Banda", "genres": ["pop", 42]}])
    assert authorized_callback(client).status_code == 502
    assert client.get("/users/1/music-profile").json()["genres"][0]["genre_name"] == "rock"
    assert db.query(Genre).count() == 1


def test_original_manual_genre_routes_work_with_personalization(client, db):
    genre_id = client.post("/genres/", json={"genre_name": "Rock"}).json()["genre_id"]
    assert len(client.get("/genres/").json()) == 1
    assert client.post(f"/users/1/genres/{genre_id}").status_code == 200
    assert client.get("/users/1/music-profile").json()["genres"][0]["sources"] == ["manual"]
    assert client.delete(f"/users/1/genres/{genre_id}").status_code == 200
    assert client.get("/users/1/music-profile").json()["genres"] == []
