from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.event_artist import event_artist
from app.models.user_event import user_event

class Event(Base):
    """
    Model representing an event in the database.

    An event can:
    - Have multiple artists (many-to-many)
    - Have multiple users (many-to-many)

    """
    __tablename__ = "events"

    # Entity attributes
    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(150), index=True)
    event_description = Column(String(500), index=True)
    event_date = Column(Date)
    ticket_link = Column(String(255), nullable=True)
    event_location = Column(String(255), nullable=True)
    organizer_id = Column(Integer, ForeignKey("organizers.organizer_id"))


    #Relationship with organizer
    organizer = relationship(
        "Organizer",
        back_populates="events"
    )

    #Relationship with user
    participants = relationship(
        "User",
        secondary=user_event,
        back_populates="events"
    )

    #Relationship with artist
    artists = relationship(
    "Artist",
    secondary=event_artist,
    back_populates="events"
    )