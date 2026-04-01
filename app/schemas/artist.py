from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from app.schemas.genre import GenreResponse


class ArtistBase(BaseModel):
    """
        Schema base do artista.

        Contém os campos utilizados nos schemas de criação,
        retorno e atualização de artistas.
    """
    artist_name: str

class ArtistCreate(ArtistBase):
    """
        Schema usada para criar o artista.
    """
    artist_name: str
    genres: list[str] = []

class ArtistResponse(ArtistBase):
    """
        Schema usada ao requisitar informações do artista.
    """
    artist_id: int
    artist_name: str
    genres: List[GenreResponse]

    class Config:
        from_attributes = True

class ArtistUpdate(BaseModel):
    """
        Schema usada para atualizar um artista existente.
        Todos os campos são opcionais
    """
    artist_name: Optional[str] = None

ArtistResponse.model_rebuild()