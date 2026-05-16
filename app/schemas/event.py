from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

from app.schemas.artist import ArtistResponse
from app.schemas.organizer import OrganizerResponse


class EventBase(BaseModel):
    """
    Base event schema.

    Contains the fields used in event creation, response, and update schemas.
    """
    event_name: str
    event_description: str
    event_date: date
    ticket_link: str
    event_location: str

class EventCreate(EventBase):
    #Schema used to create an event.
    organizer_id: int
    artists: list[str] = Field(default_factory=list)

class EventResponse(EventBase):
    #Schema used when requesting event information.
    event_id: int
    artists: List[ArtistResponse] = []
    organizer: OrganizerResponse

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    """
    Schema used to update an existing event.
    All fields are optional.
    """
    event_name: Optional[str] = None
    event_description: Optional[str] = None
    event_date: Optional[date] = None
    ticket_link: Optional[str] = None
    event_location: Optional[str] = None

EventResponse.model_rebuild()