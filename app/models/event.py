from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.event_artist import event_artist
from app.models.user_event import user_event


class Event(Base):
    """
    Modelo de evento no banco de dados.

    Um evento pode:
    - Possuir vários artistas em uma relação muitos para muitos.
    - Possuir vários usuários em uma relação muitos para muitos.
    """

    __tablename__ = "events"

    # Atributos da entidade
    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(150), index=True)
    event_description = Column(String(500), index=True)
    event_date = Column(Date)
    ticket_link = Column(String(255), nullable=True)
    event_location = Column(String(255), nullable=True)
    organizer_id = Column(Integer, ForeignKey("organizers.organizer_id"))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    notifications = relationship(
        "Notification", cascade="all, delete-orphan", back_populates="event"
    )

    # Relacionamento com o organizador
    organizer = relationship("Organizer", back_populates="events")

    # Relacionamento com os usuários
    participants = relationship("User", secondary=user_event, back_populates="events")

    # Relacionamento com os artistas
    artists = relationship("Artist", secondary=event_artist, back_populates="events")
