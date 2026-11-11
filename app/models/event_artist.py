from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database.base import Base

"""
Tabela associativa entre evento e artista.

Implementa a relação muitos para muitos entre eventos e artistas.
Cada registro representa a associação de um evento a um artista.
"""
event_artist = Table(
    "event_artist",
    Base.metadata,
    # Identificador do evento
    Column("event_id", ForeignKey("events.event_id"), primary_key=True),
    # Identificador do artista
    Column("artist_id", ForeignKey("artists.artist_id"), primary_key=True),
)
