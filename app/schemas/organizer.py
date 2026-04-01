from typing import Optional

from pydantic import BaseModel

class OrganizerBase(BaseModel):
    """
       Schema base do organizador.

       Contém os campos utilizados nos schemas de criação,
       retorno e atualização de organizadores.
    """
    organizer_name: str

class OrganizerCreate(OrganizerBase):
    """
       Schema usada para criar o organizador.
    """
    organizer_name: str

class OrganizerResponse(OrganizerBase):
    """
        Schema usada ao requisitar informações do organizador.
    """
    organizer_id: int

    class Config:
        from_attributes = True

class OrganizerUpdate(BaseModel):
    """
        Schema usada para atualizar um organizador existente.
        Todos os campos são opcionais
    """
    organizer_name: Optional[str] = None

OrganizerResponse.model_rebuild()