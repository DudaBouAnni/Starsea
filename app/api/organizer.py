from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models.organizer import Organizer
from app.schemas.event import EventResponse
from app.schemas.organizer import OrganizerCreate, OrganizerResponse, OrganizerUpdate
from app.services.organizer_service import (
    create_organizer_service,
    delete_organizer_service,
    get_organizer_events_service,
    list_organizers_service,
    update_organizer_service,
)

router = APIRouter(prefix="/organizers", tags=["organizers"])


# Cria um organizador
@router.post("/", response_model=OrganizerResponse)
def create_organizer(organizer: OrganizerCreate, db: Session = Depends(get_db)):
    """
    Cria um organizador no banco de dados.

    - **organizer_name**: nome do organizador.
    """

    return create_organizer_service(organizer, db)


# Lista os organizadores
@router.get("/", response_model=List[OrganizerResponse])
def list_organizers(db: Session = Depends(get_db)):
    """
    Retorna as informações dos organizadores cadastrados no banco.

    - **organizer_name**: nome do organizador.
    - **organizer_id**: identificador do organizador.
    """
    return list_organizers_service(db)


# Lista os eventos do organizador
@router.get("/{organizer_id}/events", response_model=list[EventResponse])
def get_organizer_events(organizer_id: int, event_id: int, db: Session = Depends(get_db)):
    """
    Retorna os eventos do organizador.

    - **organizer_id**: identificador do organizador.

    Localiza o organizador pelo identificador e retorna sua lista de eventos.
    """

    return get_organizer_events_service(organizer_id, db)


# Atualiza o organizador
@router.patch("/{organizer_id}")
def update_organizer(
    organizer_id: int, updated_data: OrganizerUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza os dados do organizador.

    - **organizer_id**: identificador do organizador.

    Localiza o organizador pelo identificador e permite atualizar seus dados.
    """

    return update_organizer_service(organizer_id, updated_data, db)


# Exclui o organizador
@router.delete("/{organizer_id}")
def delete_organizer(organizer_id: int, db: Session = Depends(get_db)):
    """
    Exclui o organizador do banco de dados.

    - **organizer_id**: identificador do organizador.

    Localiza o organizador pelo identificador e remove seu registro.
    """

    return delete_organizer_service(organizer_id, db)
