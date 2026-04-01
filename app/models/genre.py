from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.artist_genre import artist_genre
from app.models.user_genre import user_genre


class Genre(Base):
    """
    Modelo que representa um gênero no banco de dados.

    Um gênero pode:
    - Possuir vários artistas (many-to-many)
    - Possuir vários usuários (many-to-many)
    """
    __tablename__ = "genres"

    #Atributos da entidade
    genre_id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String, index=True)

    #Relação com artist
    artists = relationship(
        "Artist",
        secondary=artist_genre,
        back_populates="genres"
    )

    #Relação com user
    users = relationship(
        "User",
        secondary=user_genre,
        back_populates="genres"
    )