from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from app.schemas.genre import GenreResponse


class ArtistBase(BaseModel):
    """
    Base artist schema.

    Contains the fields used in artist creation, response, and update schemas.
    """
    artist_name: str

class ArtistCreate(ArtistBase):
    #Schema used to create an artist.
    artist_name: str
    genres: list[str] = []

class ArtistResponse(ArtistBase):
    #Schema used when requesting artist information.
    artist_id: int
    artist_name: str
    genres: List[GenreResponse]

    class Config:
        from_attributes = True

class ArtistUpdate(BaseModel):
    """
    Schema used to update an existing artist.
    All fields are optional.
    """
    artist_name: Optional[str] = None

ArtistResponse.model_rebuild()