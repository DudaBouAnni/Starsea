from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.artist_genre import artist_genre
from app.models.user_genre import user_genre


class Genre(Base):
    """
    Model representing a genre in the database.

    A genre can:
    - Have multiple artists (many-to-many)
    - Have multiple users (many-to-many)

    """
    __tablename__ = "genres"

    #Entity attributes
    genre_id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String, index=True)

    #Relationship with artist
    artists = relationship(
        "Artist",
        secondary=artist_genre,
        back_populates="genres"
    )

    #Relationship with user
    users = relationship(
        "User",
        secondary=user_genre,
        back_populates="genres"
    )