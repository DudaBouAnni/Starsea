from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

"""
Association table between User and Genre.

Responsible for implementing the many-to-many relationship between users and genres.
Each record represents the association between a user and a genre.

"""
user_genre = Table(
    "user_genre",
    Base.metadata,
    #User ID
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    #Genre ID
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True)
)