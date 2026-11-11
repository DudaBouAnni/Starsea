from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.artist_genre import artist_genre
from app.models.event_artist import event_artist
from app.models.music_genre import artist_spotify_genre


class Artist(Base):
    """
    Modelo de artista no banco de dados.

    Um artista pode:
    - Participar de vários eventos em uma relação muitos para muitos.
    - Possuir vários gêneros musicais em uma relação muitos para muitos.
    """

    __tablename__ = "artists"

    # Atributos da entidade
    artist_id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String(255), index=True)
    spotify_id = Column(String(255), nullable=True, unique=True)
    music_preferences = relationship(
        "MusicPreference", cascade="all, delete-orphan", back_populates="artist"
    )

    # Relacionamento com os eventos
    events = relationship("Event", secondary=event_artist, back_populates="artists")

    # Relacionamento com os gêneros
    genres = relationship("Genre", secondary=artist_genre, back_populates="artists")
    spotify_genres = relationship(
        "Genre", secondary=artist_spotify_genre, back_populates="spotify_artists"
    )
