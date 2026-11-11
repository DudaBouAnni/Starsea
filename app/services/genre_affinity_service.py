"""Estima a afinidade por gênero com base no ranking de artistas, sem contar reproduções."""

from app.models import Artist, User
from app.schemas.music import PreferredGenre

MAX_INFERRED_GENRES = 5


def artist_genres(artist: Artist):
    return {genre.genre_id: genre for genre in [*artist.genres, *artist.spotify_genres]}


def preference_genres(preference):
    if preference.source == "spotify":
        # Na ausência de metadados do provedor, utiliza apenas gêneros curados do catálogo.
        return preference.genres or preference.artist.genres
    return list(artist_genres(preference.artist).values())


def genre_affinities(user: User) -> list[PreferredGenre]:
    scores = {}
    selected = {}
    # Um artista também selecionado manualmente não deve ser contado duas vezes.
    for preference in user.music_preferences:
        current = selected.get(preference.artist_id)
        if current is None or preference.source == "spotify":
            selected[preference.artist_id] = preference
    for preference in selected.values():
        genres = {genre.genre_id: genre for genre in preference_genres(preference)}
        if not genres:
            continue
        weight = 1 / max(preference.rank or 1, 1) if preference.source == "spotify" else 1
        source = (
            "spotify" if preference.source == "spotify" and preference.genres else "artist_catalog"
        )
        for genre in genres.values():
            entry = scores.setdefault(
                genre.genre_id, {"genre": genre, "score": 0.0, "artists": set(), "sources": set()}
            )
            # Divide o peso entre os gêneros para não favorecer artistas com muitas classificações.
            entry["score"] += weight / len(genres)
            entry["artists"].add(preference.artist_id)
            entry["sources"].add(source)
    manual_ids = {genre.genre_id for genre in user.genres}
    for genre in user.genres:
        entry = scores.setdefault(
            genre.genre_id, {"genre": genre, "score": 0.0, "artists": set(), "sources": set()}
        )
        entry["score"] += 1
        entry["sources"].add("manual")
    ordered = sorted(
        scores.values(),
        key=lambda item: (
            -item["score"],
            item["genre"].genre_name.casefold(),
            item["genre"].genre_id,
        ),
    )
    total = sum(item["score"] for item in ordered)
    return [
        PreferredGenre(
            genre_id=item["genre"].genre_id,
            genre_name=item["genre"].genre_name,
            score=round(item["score"], 6),
            affinity_percent=round(100 * item["score"] / total, 2),
            artist_count=len(item["artists"]),
            sources=sorted(item["sources"]),
            used_for_recommendations=index < MAX_INFERRED_GENRES
            or item["genre"].genre_id in manual_ids,
        )
        for index, item in enumerate(ordered)
    ]


def preferred_genre_ids(user: User) -> set[int]:
    return {genre.genre_id for genre in genre_affinities(user) if genre.used_for_recommendations}


def genre_data_status(user: User) -> str:
    if not user.music_preferences:
        return "manual" if user.genres else "unavailable"
    preferences = list(user.music_preferences)
    available = sum(bool(preference_genres(preference)) for preference in preferences)
    if not available:
        return "partial" if user.genres else "unavailable"
    return "available" if available == len(preferences) else "partial"
