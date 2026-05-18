from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.exceptions.ConflictException import ConflitException
from app.exceptions.NotFoundException import NotFoundException
from app.models.organizer import Organizer
from app.schemas.event import EventResponse
from app.schemas.organizer import OrganizerCreate, OrganizerResponse, OrganizerUpdate
from typing import List

from app.services.organizer_service import create_organizer_service, list_organizers_service, \
    get_organizer_events_service, update_organizer_service, delete_organizer_service

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

    return create_organizer_service(organizer, db)

#List all organizers
@router.get("/", response_model=List[OrganizerResponse])
def list_organizers(
    db: Session = Depends(get_db)):
    """
        Returns the following information for all organizers registered in the DB:

        - **organizer_name**: returns organizer name
        - **organizer_id**: returns organizer ID

    """
    return list_organizers_service(db)

#Lists all events from an organizer
@router.get("/{organizer_id}/events", response_model=list[EventResponse])
def get_organizer_events (
        organizer_id: int,
        event_id: int,
        db: Session = Depends(get_db)):
    """
        Returns all os events from an organizer:

        - **organizer_id**: receive organizer ID

        Finds organizer by its ID and returns the organizer's event list

    """

    return get_organizer_events_service(organizer_id, db)

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

    return update_organizer_service(organizer_id, updated_data, db)

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

    return delete_organizer_service(organizer_id, db)