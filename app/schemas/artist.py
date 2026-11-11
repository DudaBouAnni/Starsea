from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.genre import GenreResponse


class ArtistBase(BaseModel):
    """
    Esquema base de artista.

    Define os campos utilizados na criação, nas respostas e na atualização de artistas.
    """

    artist_name: str
    spotify_id: str | None = Field(None, min_length=1, max_length=255, pattern=r"^[A-Za-z0-9]+$")


class ArtistCreate(ArtistBase):
    # Esquema de dados para criar um artista.
    artist_name: str
    genres: list[str] = []


class ArtistResponse(ArtistBase):
    # Esquema de resposta com os dados do artista.
    artist_id: int
    artist_name: str
    genres: List[GenreResponse]

    model_config = ConfigDict(from_attributes=True)


class ArtistUpdate(BaseModel):
    """
    Esquema para atualizar um artista existente.
    Todos os campos são opcionais.
    """

    artist_name: Optional[str] = None
    spotify_id: str | None = Field(None, min_length=1, max_length=255, pattern=r"^[A-Za-z0-9]+$")


ArtistResponse.model_rebuild()
