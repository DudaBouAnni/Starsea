from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.event import EventResponse


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
