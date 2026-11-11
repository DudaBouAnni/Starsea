"""Gerenciamento do gosto musical e descoberta personalizada de eventos."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.music import MusicProfile, RecommendedEvent
from app.services.maps_service import event_map_url
from app.services.music_match_service import has_music_match, matched_artists, matched_genres
from app.services.music_service import (
    get_music_profile,
    remove_music_source,
    select_manual_artist,
    select_manual_genre,
)
from app.services.nearby_service import get_user, nearby_events

router = APIRouter(prefix="/users", tags=["musical taste"])


@router.get("/{user_id}/music-profile", response_model=MusicProfile)
def music_profile(user_id: int, db: Session = Depends(get_db)):
    return get_music_profile(user_id, db)


@router.put("/{user_id}/music-profile/artists/{artist_id}", response_model=MusicProfile)
def choose_artist(user_id: int, artist_id: int, db: Session = Depends(get_db)):
    """Seleciona um artista manualmente, inclusive para quem usa YouTube Music."""
    return select_manual_artist(user_id, artist_id, db)


@router.delete("/{user_id}/music-profile/artists/{artist_id}", response_model=MusicProfile)
def unchoose_artist(user_id: int, artist_id: int, db: Session = Depends(get_db)):
    """Remove somente a escolha manual; não altera o snapshot do Spotify."""
    return remove_music_source(user_id, "manual", db, artist_id)


@router.delete("/{user_id}/music-profile/spotify", response_model=MusicProfile)
def clear_spotify_profile(user_id: int, db: Session = Depends(get_db)):
    """Apaga as preferências importadas. A autorização pode ser revogada na conta Spotify."""
    return remove_music_source(user_id, "spotify", db)


@router.put("/{user_id}/music-profile/genres/{genre_id}", response_model=MusicProfile)
def choose_genre(user_id: int, genre_id: int, db: Session = Depends(get_db)):
    return select_manual_genre(user_id, genre_id, db, selected=True)


@router.delete("/{user_id}/music-profile/genres/{genre_id}", response_model=MusicProfile)
def unchoose_genre(user_id: int, genre_id: int, db: Session = Depends(get_db)):
    return select_manual_genre(user_id, genre_id, db, selected=False)


@router.get("/{user_id}/recommended-events", response_model=list[RecommendedEvent])
def recommended_events(
    user_id: int,
    radius_km: float | None = Query(None, gt=0, le=1000, allow_inf_nan=False),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Shows próximos por artista ou gênero preferido, com o motivo de cada recomendação."""
    user = get_user(user_id, db)
    matches = [
        (event, distance)
        for event, distance in nearby_events(user, db, radius_km or user.notification_radius_km)
        if has_music_match(user, event)
    ]
    return [
        RecommendedEvent(
            event=event,
            distance_km=round(distance, 2),
            maps_url=event_map_url(event),
            matched_artists=matched_artists(user, event),
            matched_genres=matched_genres(user, event),
            match_reasons=(["artist"] if matched_artists(user, event) else [])
            + (["genre"] if matched_genres(user, event) else []),
        )
        for event, distance in matches[offset : offset + limit]
    ]
