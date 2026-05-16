from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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

#Creates organizer
@router.post("/", response_model=OrganizerResponse)
def create_organizer(
        organizer: OrganizerCreate,
        db: Session = Depends(get_db)):
    """
       Creates an organizer in the DB:

        - **organizer_name**: receives organizer name

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

#List all organizers
@router.get("/", response_model=List[OrganizerResponse])
def list_organizers(
    db: Session = Depends(get_db)):
    """
        Returns the following information for all organizers registered in the DB:

        - **organizer_name**: returns organizer name
        - **organizer_id**: returns organizer ID

    """
    return db.query(Organizer).all()

#Lists all events from an organizer
@router.get("/{organizer_id}/events", response_model=list[EventResponse])
def get_organizer_events (
        organizer_id: int,
        db: Session = Depends(get_db)):
    """
        Returns all os events from an organizer:

        - **organizer_id**: receive organizer ID

        Finds organizer by its ID and returns the organizer's event list

    """
    organizer = db.get(Organizer, organizer_id)

    #Checks if organizer exists
    if not organizer:
        raise NotFoundException("Organizer does not exist")

    return organizer.events

#Updates organizer
@router.patch("/{organizer_id}")
def update_organizer(
    organizer_id: int,
    updated_data: OrganizerUpdate,
    db: Session = Depends(get_db)):
    """
        Updates organizer information:

        - **organizer_id**: receives organizer ID

        Finds organizer by its ID and allows updating its information

    """
    organizer = db.get(Organizer, organizer_id)

    #Checks if organizer exists in the DB
    if not organizer:
        raise NotFoundException("Organizer does not exist")

    update_organizer = updated_data.model_dump(exclude_unset=True)

    for key, value in update_organizer.items():
        setattr(organizer, key, value)

    db.commit()
    db.refresh(organizer)

    return organizer

#Deletes organizer
@router.delete("/{organizer_id}")
def delete_organizer(
        organizer_id: int,
        db: Session = Depends(get_db)):
    """
        Deletes organizer:

        - **organizer_id**: receive organizer ID

        Finds organizer by its ID and deletes it from the DB

    """
    organizer = db.get(Organizer, organizer_id)

    if not organizer:
        NotFoundException("Organizer does not exist")

    organizer.events.clear()

    db.delete(organizer)
    db.commit()

    return {"message": "Organizer deleted successfully!"}