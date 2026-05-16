from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

"""
Association table between User and Event.

Responsible for implementing the many-to-many relationship between users and events.
Each record represents the association between a user and an event.

"""
user_event = Table(

    "user_event",
    Base.metadata,
    #User ID
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    #Event ID
    Column("event_id", Integer, ForeignKey("events.event_id"), primary_key=True)
)