from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

"""
Association table between Event and Artist.

Responsible for implementing the many-to-many relationship between events and artists.
Each record represents the association between an event and an artist.

"""
event_artist = Table(
    "event_artist",
    Base.metadata,

    #Event ID
    Column("event_id", ForeignKey("events.event_id"), primary_key=True),
    #Artist ID
    Column("artist_id", ForeignKey("artists.artist_id"), primary_key=True),
)