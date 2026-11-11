"""Artistas selecionados pelo usuário ou importados de um serviço de música."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.music_genre import music_preference_genre


class MusicPreference(Base):
    __tablename__ = "music_preferences"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    artist_id = Column(
        Integer, ForeignKey("artists.artist_id", ondelete="CASCADE"), primary_key=True
    )
    source = Column(String(30), primary_key=True)
    rank = Column(Integer, nullable=True)
    updated_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    user = relationship("User", back_populates="music_preferences")
    artist = relationship("Artist", back_populates="music_preferences")
    genres = relationship(
        "Genre", secondary=music_preference_genre, back_populates="music_preferences"
    )
