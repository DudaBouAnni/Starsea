from typing import Optional

from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    """
    Esquema base de gênero.

    Define os campos utilizados na criação, nas respostas e na atualização de gêneros.
    """

    genre_name: str


class GenreCreate(GenreBase):
    # Esquema de dados para criar um gênero.
    genre_name: str


class GenreResponse(GenreBase):
    # Esquema de resposta com os dados do gênero.
    genre_id: int

    model_config = ConfigDict(from_attributes=True)


class GenreUpdate(BaseModel):
    """
    Esquema para atualizar um gênero existente.
    Todos os campos são opcionais.
    """

    genre_name: Optional[str] = None


GenreResponse.model_rebuild()
