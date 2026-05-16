from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Organizer(Base):
    """
    Model representing an organizer in the database.

    An organizer can:
    - Have multiple events (many-to-many)

    """
    __tablename__ = "organizers"

    #Entity attributes
    organizer_id = Column(Integer, primary_key=True, index=True)
    organizer_name = Column(String(255), nullable=False)

    #Relationship with event
    events = relationship(
        "Event",
        back_populates="organizer")