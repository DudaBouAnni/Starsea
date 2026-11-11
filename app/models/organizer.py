from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Organizer(Base):
    """
    Modelo de organizador no banco de dados.

    Um organizador pode ser associado a vários eventos.
    """

    __tablename__ = "organizers"

    # Atributos da entidade
    organizer_id = Column(Integer, primary_key=True, index=True)
    organizer_name = Column(String(255), nullable=False)

    # Relacionamento com os eventos
    events = relationship("Event", back_populates="organizer")
