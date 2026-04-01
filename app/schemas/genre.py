from typing import Optional

from pydantic import BaseModel

class GenreBase(BaseModel):
    """
        Schema base do gênero.

        Contém os campos utilizados nos schemas de criação,
        retorno e atualização de gêneros.
    """
    genre_name: str

class GenreCreate(GenreBase):
    """
        Schema usada para criar o gênero.
    """
    genre_name: str

class GenreResponse(GenreBase):
    """
        Schema usada ao requisitar informações do gênero.
    """
    genre_id: int

    class Config:
        from_attributes = True

class GenreUpdate(BaseModel):
    """
        Schema usada para atualizar um gênero existente.
        Todos os campos são opcionais
    """
    genre_name: Optional[str] = None

GenreResponse.model_rebuild()