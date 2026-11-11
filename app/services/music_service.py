"""Gerencia as preferências de artistas e sincroniza os avisos personalizados."""

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.exceptions.NotFoundException import NotFoundException
from app.models import Artist, Genre, MusicPreference, User
from app.schemas.music import MusicProfile, PreferredArtist
from app.services.genre_affinity_service import (
    genre_affinities,
    genre_data_status,
    preference_genres,
)
from app.services.music_match_service import normalized_artist_name
from app.services.nearby_service import get_user, sync_all_notifications, sync_user_notifications


def get_music_profile(user_id: int, db: Session) -> MusicProfile:
    user = get_user(user_id, db)
    preferences = db.query(MusicPreference).filter_by(user_id=user_id).all()
    preferences.sort(key=lambda item: (item.source, item.rank or 0, item.artist_id))
    return MusicProfile(
        user_id=user_id,
        personalized_notifications_only=user.personalized_notifications_only,
        spotify_preferences_synced_at=user.spotify_preferences_synced_at,
        genres=genre_affinities(user),
        genre_data_status=genre_data_status(user),
        artists=[
            PreferredArtist(
                artist_id=item.artist_id,
                artist_name=item.artist.artist_name,
                spotify_id=item.artist.spotify_id,
                spotify_url=f"https://open.spotify.com/artist/{item.artist.spotify_id}"
                if item.artist.spotify_id
                else None,
                source=item.source,
                rank=item.rank,
                updated_at=item.updated_at,
                genres=sorted({genre.genre_name for genre in preference_genres(item)}),
            )
            for item in preferences
        ],
    )


def _resolve_spotify_artist(item: dict, db: Session) -> Artist:
    existing = db.query(Artist).filter_by(spotify_id=item["id"]).first()
    if existing is not None:
        return existing
    # Vincula nomes normalizados apenas quando houver uma correspondência exata e única.
    all_names = [
        artist
        for artist in db.query(Artist).all()
        if normalized_artist_name(artist.artist_name) == normalized_artist_name(item["name"])
    ]
    if len(all_names) == 1 and all_names[0].spotify_id is None:
        artist = all_names[0]
        artist.spotify_id = item["id"]
    else:
        artist = Artist(artist_name=item["name"], spotify_id=item["id"])
        db.add(artist)
    db.flush()
    return artist


def import_spotify_artists(user: User, items: list[dict], db: Session) -> int:
    """Substitui apenas os dados do Spotify, preservando escolhas manuais e a transação atual."""
    # Valida toda a resposta antes de excluir as preferências importadas anteriormente.
    if not isinstance(items, list) or any(
        not isinstance(item, dict)
        or not isinstance(item.get("id"), str)
        or not item["id"].isascii()
        or not item["id"].isalnum()
        or len(item["id"]) > 255
        or not isinstance(item.get("name"), str)
        or not item["name"].strip()
        or len(item["name"]) > 255
        for item in items
    ):
        raise HTTPException(502, "O Spotify retornou uma lista de artistas inválida.")
    genre_snapshots = [_validated_genres(item) for item in items]
    db.flush()
    for preference in (
        db.query(MusicPreference).filter_by(user_id=user.user_id, source="spotify").all()
    ):
        db.delete(preference)
    db.flush()
    seen = set()
    for rank, (item, names) in enumerate(zip(items, genre_snapshots), 1):
        if item["id"] in seen:
            continue
        seen.add(item["id"])
        artist = _resolve_spotify_artist(item, db)
        genres = [_resolve_genre(name, db) for name in (names or [])]
        if names is not None:
            # Os metadados do provedor nunca substituem os gêneros cadastrados manualmente.
            artist.spotify_genres = genres
        db.add(
            MusicPreference(
                user_id=user.user_id,
                artist_id=artist.artist_id,
                source="spotify",
                rank=rank,
                genres=genres,
            )
        )
    # A primeira importação ativa os avisos personalizados por gosto musical.
    if user.spotify_preferences_synced_at is None:
        user.personalized_notifications_only = True
    user.spotify_preferences_synced_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.flush()
    db.expire(user, ["music_preferences"])
    sync_all_notifications(db)
    return len(seen)


def _validated_genres(item: dict) -> list[str] | None:
    raw = item.get("genres")
    if raw is None:
        return None
    if not isinstance(raw, list) or any(
        not isinstance(name, str) or not name.strip() or len(name) > 100 for name in raw
    ):
        raise HTTPException(502, "O Spotify retornou gêneros inválidos.")
    return sorted({normalized_artist_name(name) for name in raw})


def _resolve_genre(name: str, db: Session) -> Genre:
    existing = next(
        (
            genre
            for genre in db.query(Genre).order_by(Genre.genre_id).all()
            if normalized_artist_name(genre.genre_name) == name
        ),
        None,
    )
    if existing is not None:
        return existing
    genre = Genre(genre_name=name)
    db.add(genre)
    db.flush()
    return genre


def select_manual_artist(user_id: int, artist_id: int, db: Session) -> MusicProfile:
    user = get_user(user_id, db)
    if db.get(Artist, artist_id) is None:
        raise NotFoundException("Artist not found")
    preference = db.get(MusicPreference, (user_id, artist_id, "manual"))
    if preference is None:
        db.add(MusicPreference(user_id=user_id, artist_id=artist_id, source="manual"))
    user.personalized_notifications_only = True
    db.flush()
    db.expire(user, ["music_preferences"])
    sync_user_notifications(user, db)
    db.commit()
    return get_music_profile(user_id, db)


def select_manual_genre(user_id: int, genre_id: int, db: Session, selected: bool) -> MusicProfile:
    user = get_user(user_id, db)
    genre = db.get(Genre, genre_id)
    if genre is None:
        raise NotFoundException("Genre not found")
    if selected:
        if genre not in user.genres:
            user.genres.append(genre)
        user.personalized_notifications_only = True
    elif genre in user.genres:
        user.genres.remove(genre)
    sync_user_notifications(user, db)
    db.commit()
    return get_music_profile(user_id, db)


def remove_music_source(user_id: int, source: str, db: Session, artist_id: int | None = None):
    user = get_user(user_id, db)
    query = db.query(MusicPreference).filter_by(user_id=user_id, source=source)
    if artist_id is not None:
        query = query.filter_by(artist_id=artist_id)
    for preference in query.all():
        db.delete(preference)
    if source == "spotify":
        user.spotify_preferences_synced_at = None
    db.flush()
    db.expire(user, ["music_preferences"])
    # Mantém o filtro ativo: um perfil vazio não deve passar a receber avisos de todos os shows.
    sync_user_notifications(user, db)
    db.commit()
    return get_music_profile(user_id, db)
