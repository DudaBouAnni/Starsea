from fastapi import APIRouter, Depends
from app.database.session import SessionLocal
from app.exceptions.ConflictException import ConflitException
from app.exceptions.NotFoundException import NotFoundException
from app.models.organizer import Organizer
from app.schemas.event import EventResponse
from app.schemas.organizer import OrganizerCreate, OrganizerResponse, OrganizerUpdate
from typing import List

router = APIRouter(prefix="/organizers", tags=["organizers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Insere organizer
@router.post("/", response_model=OrganizerResponse)
def create_organizer(
        organizer: OrganizerCreate,
        db: Session = Depends(get_db)):
    """
       Cria um organizador no banco de dados:

        - **organizer_name**: recebe nome do organizador

    """

    # Busca event pelo organizer_name
    exists = db.query(Organizer).filter_by(
        event_name=organizer.organizer_name
    ).first()

    if exists:
        raise ConflitException("Organizer already exists")

    db_organizer = Organizer(
        organizer_name=organizer.organizer_name
    )

    db.add(db_organizer)
    db.commit()
    db.refresh(db_organizer)

    return db_organizer

#Lista todos os organizers
@router.get("/", response_model=List[OrganizerResponse])
def list_organizers(
    db: Session = Depends(get_db)):
    """
        Retorna as seguintes informações de todos os organizadores cadastrados no banco de dados:

        - **organizer_name**: retorna nome do organizador
        - **organizer_id**: retorna o id do organizador

    """
    return db.query(Organizer).all()

#Lista todos os eventos de algum organinzer
@router.get("/{organizer_id}/events", response_model=list[EventResponse])
def get_organizer_events (
        organizer_id: int,
        db: Session = Depends(get_db)):
    """
        Retorna todos os eventos de algum organizador:

        - **organizer_id**: recebe id do organizador

        Localiza organizador pelo id e retorna a lista de eventos do organizador

    """
    organizer = db.get(Organizer, organizer_id)

    #Verifica se organizer existe
    if not organizer:
        raise NotFoundException("Organizer does not exist")

    return organizer.events

#Atualiza organizer
@router.patch("/{organizer_id}")
def update_organizer(
    organizer_id: int,
    updated_data: OrganizerUpdate,
    db: Session = Depends(get_db)):
    """
        Atualiza informações do organizador:

        - **organizer_id**: id nome do organizador

        Localiza organizador pelo id e permite alterações nas informações

    """
    organizer = db.get(Organizer, organizer_id)

    #Verifica se organizador existe no db
    if not organizer:
        raise NotFoundException("Organizer does not exist")

    update_organizer = updated_data.model_dump(exclude_unset=True)

    for key, value in update_organizer.items():
        setattr(organizer, key, value)

    db.commit()
    db.refresh(organizer)

    return organizer

#Deleta organizer
@router.delete("/{organizer_id}")
def delete_organizer(
        organizer_id: int,
        db: Session = Depends(get_db)):
    """
        Deleta organizador:

        - **organizer_id**: recebe id do organizador

        Localiza organizador pelo id e remove o do db

    """
    organizer = db.get(Organizer, organizer_id)

    if not organizer:
        NotFoundException("Organizer does not exist")

    organizer.events.clear()

    db.delete(organizer)
    db.commit()

    return {"message": "Organizer deleted successfully!"}