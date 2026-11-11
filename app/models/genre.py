from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.artist_genre import artist_genre
from app.models.music_genre import artist_spotify_genre, music_preference_genre
from app.models.user_genre import user_genre


class Genre(Base):
    """
    Modelo de gênero no banco de dados.

    Um gênero pode:
    - Possuir vários artistas em uma relação muitos para muitos.
    - Possuir vários usuários em uma relação muitos para muitos.
    """

    __tablename__ = "genres"

    # Atributos da entidade
    genre_id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String(100), index=True)

    # Relacionamento com os artistas
    artists = relationship("Artist", secondary=artist_genre, back_populates="genres")

    # Relacionamento com os usuários
    users = relationship("User", secondary=user_genre, back_populates="genres")
    spotify_artists = relationship(
        "Artist", secondary=artist_spotify_genre, back_populates="spotify_genres"
    )
    music_preferences = relationship(
        "MusicPreference", secondary=music_preference_genre, back_populates="genres"
    )
