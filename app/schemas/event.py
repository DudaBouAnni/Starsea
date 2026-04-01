from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

from app.schemas.artist import ArtistResponse
from app.schemas.organizer import OrganizerResponse


class EventBase(BaseModel):
    """
        Schema base do evento.

        Contém os campos utilizados nos schemas de criação,
        retorno e atualização de eventos.
    """
    event_name: str
    event_description: str
    event_date: date
    ticket_link: str
    event_location: str

class EventCreate(EventBase):
    """
        Schema usada para criar o evento.
    """
    organizer_id: int
    artists: list[str] = Field(default_factory=list)

class EventResponse(EventBase):
    """
        Schema usada ao requisitar informações do evento.
    """
    event_id: int
    artists: List[ArtistResponse] = []
    organizer: OrganizerResponse

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    """
        Schema usada para atualizar um evento existente.
        Todos os campos são opcionais
    """
    event_name: Optional[str] = None
    event_description: Optional[str] = None
    event_date: Optional[date] = None
    ticket_link: Optional[str] = None
    event_location: Optional[str] = None

EventResponse.model_rebuild()