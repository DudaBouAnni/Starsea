from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.artist_genre import artist_genre
from app.models.event_artist import event_artist

class Artist(Base):

    """
    Modelo que representa um artista no banco de dados.

    Um artista pode:
    - Fazer parte de vários eventos (many-to-many)
    - Possuir vários gêneros musicais (many-to-many)
    """

    __tablename__ = "artists"

    #Atributos da entidade
    artist_id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String, index=True)

    #Relação com o event
    events = relationship(
        "Event",
        secondary=event_artist,
        back_populates="artists"
    )

    #Relação com o genre
    genres = relationship(
        "Genre",
        secondary=artist_genre,
        back_populates="artists"
    )