from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

"""
Tabela associativa entre Artist e Genre.

Responsável por implementar a relação many-to-many entre artistas e gêneros.
Cada registro representa a associação entre um artista e um gênero.
"""
artist_genre = Table(
    "artist_genre",
    Base.metadata,

    #ID do artista
    Column("artist_id", Integer, ForeignKey("artists.artist_id"), primary_key=True),

    #ID do gênero
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True)
)