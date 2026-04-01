from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.event_artist import event_artist
from app.models.user_event import user_event

class Event(Base):
    """
    Modelo que representa um evento no banco de dados.

    Um evento pode:
    - Possuir vários artistas (many-to-many)
    - Possuir vários usuários (many-to-many)
    """
    __tablename__ = "events"

    #Atributos da entidade
    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(150), index=True)
    event_description = Column(String(500), index=True)
    event_date = Column(Date)
    ticket_link = Column(String(255), nullable=True)
    event_location = Column(String(255), nullable=True)
    organizer_id = Column(Integer, ForeignKey("organizers.organizer_id"))


    #Relação com o organizer
    organizer = relationship(
        "Organizer",
        back_populates="events"
    )

    #Relação com o user
    participants = relationship(
        "User",
        secondary=user_event,
        back_populates="events"
    )

    #Relação com o artist
    artists = relationship(
    "Artist",
    secondary=event_artist,
    back_populates="events"
    )