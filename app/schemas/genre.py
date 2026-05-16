from typing import Optional

from pydantic import BaseModel

class GenreBase(BaseModel):
    """
    Base genre schema.

    Contains the fields used in genre creation, response, and update schemas.
    """
    genre_name: str

class GenreCreate(GenreBase):
    #Schema used to create a genre.
    genre_name: str

class GenreResponse(GenreBase):
    #Schema used when requesting genre information.
    genre_id: int

    class Config:
        from_attributes = True

class GenreUpdate(BaseModel):
    """
    Schema used to update an existing genre.
    All fields are optional.
    """
    genre_name: Optional[str] = None

GenreResponse.model_rebuild()