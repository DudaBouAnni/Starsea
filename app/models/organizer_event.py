from sqlalchemy import Table, Column, ForeignKey
from app.database.base import Base

"""
Tabela associativa entre Organizer e Event.

Responsável por implementar a relação many-to-many entre organizador e eventos.
Cada registro representa a associação entre um organizador e um evento.
"""
organizer_event = Table(
    "organizer_event",
    Base.metadata,
    #ID do organizador
    Column("organizer_id", ForeignKey("organizers.organizer_id"), primary_key=True),
    #ID do evento
    Column("event_id", ForeignKey("events.event_id"), primary_key=True)
)