from sqlalchemy import Table, Column, ForeignKey
from app.database.base import Base

"""
Association table between Organizer and Event.

Responsible for implementing the many-to-many relationship between organizer and events.
Each record represents the association between an organizer and an event.

"""
organizer_event = Table(
    "organizer_event",
    Base.metadata,
    #Organizer ID
    Column("organizer_id", ForeignKey("organizers.organizer_id"), primary_key=True),
    #Event ID
    Column("event_id", ForeignKey("events.event_id"), primary_key=True)
)