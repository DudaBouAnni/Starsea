from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.user_event import user_event
from app.models.user_genre import user_genre


class User(Base):
    """
    Model representing a user in the database.

    A user can:
    - Have multiple events (many-to-many)
    - Have multiple genres (many-to-many)

    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True)
    email = Column(String(225), unique=True, index=True)
    user_password = Column(String(225), unique=True, index=True)


    #Relationship with event
    events = relationship(
        "Event",
        secondary=user_event,
        back_populates="participants"
    )

    #Relationship with genre
    genres = relationship(
        "Genre",
        secondary=user_genre,
        back_populates="users")