from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

"""
Tabela associativa entre Event e Artist.

Responsável por implementar a relação many-to-many entre eventos e artistas.
Cada registro representa a associação entre um evento e um artista.
"""
event_artist = Table(
    "event_artist",
    Base.metadata,

    #ID do evento
    Column("event_id", ForeignKey("events.event_id"), primary_key=True),
    #ID do artista
    Column("artist_id", ForeignKey("artists.artist_id"), primary_key=True),
)