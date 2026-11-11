from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user_event import user_event
from app.models.user_genre import user_genre


class User(Base):
    """
    Modelo de usuário no banco de dados.

    Um usuário pode:
    - Possuir vários eventos em uma relação muitos para muitos.
    - Possuir vários gêneros em uma relação muitos para muitos.
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True)
    email = Column(String(225), unique=True, index=True)
    user_password = Column(String(225), nullable=True)
    city = Column(String(100), index=True)
    state = Column(String(100), index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    notification_radius_km = Column(Float, nullable=False, default=50.0)
    nearby_notifications_enabled = Column(Boolean, nullable=False, default=True)
    personalized_notifications_only = Column(Boolean, nullable=False, default=False)
    spotify_preferences_synced_at = Column(DateTime, nullable=True)
    music_preferences = relationship(
        "MusicPreference", cascade="all, delete-orphan", back_populates="user"
    )
    notifications = relationship(
        "Notification", cascade="all, delete-orphan", back_populates="user"
    )
    # Informações da conexão com o Spotify
    profile_image = Column(String(500), nullable=True)
    spotify_id = Column(String(255), unique=True, nullable=True)
    country = Column(String(10), nullable=True)

    # Relacionamento com os eventos
    events = relationship("Event", secondary=user_event, back_populates="participants")

    # Relacionamento com os gêneros
    genres = relationship("Genre", secondary=user_genre, back_populates="users")
