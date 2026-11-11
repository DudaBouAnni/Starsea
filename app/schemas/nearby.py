from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from app.schemas.event import EventResponse
from app.schemas.location import RadiusKm


class TravelMode(str, Enum):
    driving = "driving"
    walking = "walking"
    bicycling = "bicycling"
    transit = "transit"


class NearbyEvent(BaseModel):
    event: EventResponse
    distance_km: float
    distance_type: str = "straight_line"
    maps_url: str


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    notification_id: int
    event_id: int
    message: str
    distance_km: float
    is_read: bool
    created_at: datetime


class RouteOption(BaseModel):
    travel_mode: TravelMode
    available: bool
    maps_url: str
    distance_km: float | None = None
    duration_minutes: float | None = None
    within_distance_limit: bool | None = None
    status: str


class EventRoutes(BaseModel):
    event_id: int
    event_date: date
    straight_line_distance_km: float
    distance_limit_km: RadiusKm
    routes: list[RouteOption]
    estimates_for: str = "departure_now"
