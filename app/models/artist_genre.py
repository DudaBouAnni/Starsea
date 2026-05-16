from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

"""
Association table between Artist and Genre.

Responsible for implementing the many-to-many relationship between artists and genres.
Each record represents the association between an artist and a genre.

"""
artist_genre = Table(
    "artist_genre",
    Base.metadata,

    #Aritst ID
    Column("artist_id", Integer, ForeignKey("artists.artist_id"), primary_key=True),

    #Genre ID
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True)
)