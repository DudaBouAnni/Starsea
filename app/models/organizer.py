from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Organizer(Base):
    """
    Modelo que representa um organizador no banco de dados.

    Um organizador pode:
    - Possuir vários eventos (many-to-many)

    """
    __tablename__ = "organizers"

    #Atributos da entidade
    organizer_id = Column(Integer, primary_key=True, index=True)
    organizer_name = Column(String(255), nullable=False)

    #Relação com o event
    events = relationship(
        "Event",
        back_populates="organizer")