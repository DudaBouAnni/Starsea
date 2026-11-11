from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database.base import Base

"""
Tabela associativa entre usuário e gênero.

Implementa a relação muitos para muitos entre usuários e gêneros.
Cada registro representa a associação de um usuário a um gênero.
"""
user_genre = Table(
    "user_genre",
    Base.metadata,
    # Identificador do usuário
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    # Identificador do gênero
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True),
)
