from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.artist_genre import artist_genre
from app.models.event_artist import event_artist

class Artist(Base):

    """
    Model representing an artist in the database.

    An artist can:
    - Be part of multiple events (many-to-many)
    - Have multiple music genres (many-to-many)

    """

    __tablename__ = "artists"

    #Entity attributes
    artist_id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String, index=True)

    #Relationship with event
    events = relationship(
        "Event",
        secondary=event_artist,
        back_populates="artists"
    )

    #Relationship with genre
    genres = relationship(
        "Genre",
        secondary=artist_genre,
        back_populates="artists"
    )