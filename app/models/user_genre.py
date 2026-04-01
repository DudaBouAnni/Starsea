from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

"""
Tabela associativa entre User e Genre.

Responsável por implementar a relação many-to-many entre usuários e gêneros.
Cada registro representa a associação entre um usuário e um gênero.
"""
user_genre = Table(
    "user_genre",
    Base.metadata,
    #ID do usuário
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    #ID do gênero
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True)
)