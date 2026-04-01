from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.user_event import user_event
from app.models.user_genre import user_genre


class User(Base):
    """
    Modelo que representa um usuário no banco de dados.

    Um usuário pode:
    - Possuir vários eventos (many-to-many)
    - Possuir vários gêneros (many-to-many)
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True)
    email = Column(String(225), unique=True, index=True)
    user_password = Column(String(225), unique=True, index=True)


    #Relação com event
    events = relationship(
        "Event",
        secondary=user_event,
        back_populates="participants"
    )

    #Relação com genre
    genres = relationship(
        "Genre",
        secondary=user_genre,
        back_populates="users")