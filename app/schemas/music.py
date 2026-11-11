from datetime import datetime

from pydantic import BaseModel

from app.schemas.nearby import NearbyEvent
from app.schemas.user import UserResponse


class PreferredArtist(BaseModel):
    artist_id: int
    artist_name: str
    spotify_id: str | None
    spotify_url: str | None
    source: str
    rank: int | None
    updated_at: datetime
    genres: list[str] = []


class PreferredGenre(BaseModel):
    genre_id: int
    genre_name: str
    score: float
    affinity_percent: float
    artist_count: int
    sources: list[str]
    used_for_recommendations: bool


class MusicProfile(BaseModel):
    user_id: int
    personalized_notifications_only: bool
    spotify_preferences_synced_at: datetime | None
    artists: list[PreferredArtist]
    genres: list[PreferredGenre] = []
    genre_data_status: str = "unavailable"
    genre_estimation_method: str = "artist_affinity_weighted"


class RecommendedEvent(NearbyEvent):
    matched_artists: list[str]
    matched_genres: list[str]
    match_reasons: list[str]


class SpotifyLoginResponse(BaseModel):
    message: str
    user: UserResponse
    imported_artists: int
