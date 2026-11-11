from sqlalchemy import Column, ForeignKey, Table

from app.database.base import Base

"""
Tabela associativa entre organizador e evento.

Representa uma relação muitos para muitos entre organizadores e eventos.
Cada registro associa um organizador a um evento.
"""
organizer_event = Table(
    "organizer_event",
    Base.metadata,
    # Identificador do organizador
    Column("organizer_id", ForeignKey("organizers.organizer_id"), primary_key=True),
    # Identificador do evento
    Column("event_id", ForeignKey("events.event_id"), primary_key=True),
)
