from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrganizerBase(BaseModel):
    """
    Esquema base de organizador.

    Define os campos utilizados na criação, nas respostas e na atualização de organizadores.
    """

    organizer_name: str


class OrganizerCreate(OrganizerBase):
    # Esquema de dados para criar um organizador.
    organizer_name: str


class OrganizerResponse(OrganizerBase):
    # Esquema de resposta com os dados do organizador.
    organizer_id: int

    model_config = ConfigDict(from_attributes=True)


class OrganizerUpdate(BaseModel):
    """
    Esquema para atualizar um organizador existente.
    Todos os campos são opcionais.
    """

    organizer_name: Optional[str] = None


OrganizerResponse.model_rebuild()
