"""Cruza as preferências com o catálogo local sem consultar o provedor por HTTP."""

import unicodedata

from sqlalchemy import or_

from app.models import Artist, Event, Genre, User
from app.services.genre_affinity_service import artist_genres, preferred_genre_ids


def normalized_artist_name(name: str) -> str:
    # Preserva acentos e pontuação para não confundir artistas diferentes.
    return " ".join(unicodedata.normalize("NFKC", name).casefold().split())


def matched_artists(user: User, event: Event) -> list[str]:
    preferred_ids = {preference.artist_id for preference in user.music_preferences}
    return sorted(
        {artist.artist_name for artist in event.artists if artist.artist_id in preferred_ids}
    )


def matches_music_preferences(user: User, event: Event) -> bool:
    return not user.personalized_notifications_only or has_music_match(user, event)


def matched_genres(user: User, event: Event) -> list[str]:
    preferred = preferred_genre_ids(user)
    return sorted(
        {
            genre.genre_name
            for artist in event.artists
            for genre in artist_genres(artist).values()
            if genre.genre_id in preferred
        }
    )


def has_music_match(user: User, event: Event) -> bool:
    return bool(matched_artists(user, event) or matched_genres(user, event))


def music_event_filter(user: User):
    """Equivalente SQL de has_music_match, aplicado antes da paginação de notificações."""
    artists = {item.artist_id for item in user.music_preferences}
    genres = preferred_genre_ids(user)
    return Event.artists.any(
        or_(
            Artist.artist_id.in_(artists),
            Artist.genres.any(Genre.genre_id.in_(genres)),
            Artist.spotify_genres.any(Genre.genre_id.in_(genres)),
        )
    )
