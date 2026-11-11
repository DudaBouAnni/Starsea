from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database.base import Base

"""
Tabela associativa entre artista e gênero.

Implementa a relação muitos para muitos entre artistas e gêneros.
Cada registro representa a associação de um artista a um gênero.
"""
artist_genre = Table(
    "artist_genre",
    Base.metadata,
    # Identificador do artista
    Column("artist_id", Integer, ForeignKey("artists.artist_id"), primary_key=True),
    # Identificador do gênero
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True),
)
