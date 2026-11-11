from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.artist import ArtistResponse
from app.schemas.location import OptionalCoordinates
from app.schemas.organizer import OrganizerResponse


class EventBase(OptionalCoordinates):
    """
    Esquema base de evento.

    Define os campos utilizados na criação, nas respostas e na atualização de eventos.
    """

    event_name: str
    event_description: str
    event_date: date
    ticket_link: str
    event_location: str


class EventCreate(EventBase):
    # Esquema de dados para criar um evento.
    organizer_id: int
    artists: list[str] = Field(default_factory=list)


class EventResponse(EventBase):
    # Esquema de resposta com os dados do evento.
    event_id: int
    artists: List[ArtistResponse] = []
    organizer: OrganizerResponse

    model_config = ConfigDict(from_attributes=True)


class EventUpdate(OptionalCoordinates):
    """
    Esquema para atualizar um evento existente.
    Todos os campos são opcionais.
    """

    event_name: Optional[str] = None
    event_description: Optional[str] = None
    event_date: Optional[date] = None
    ticket_link: Optional[str] = None
    event_location: Optional[str] = None


EventResponse.model_rebuild()
