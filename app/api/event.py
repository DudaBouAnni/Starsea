from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import SessionLocal
from app.schemas.event import EventResponse, EventCreate, EventUpdate
from app.services.event_service import create_event_service, list_events_service, \
    get_event_artists_service, add_artist_event_service, update_event_service, delete_event_service, \
    remove_artist_event_service

router = APIRouter(prefix="/events", tags=["events"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create Event
@router.post("/", response_model=EventResponse)
def create_event(
        event: EventCreate,
        db: Session = Depends(get_db)):
    """
        Creates a new event in the DB:

        - **event_name**: receives event name
        - **event_description**: receives event description
        - **event_date**: receives event date
        - **ticket_link**: receives official ticket sales website link for the event
        - **event_location**: receives event location
        - **organizer_id**: receives event organizer ID
        - **artists**: receives a list of the artists participating in the event

    """
    return create_event_service(event, db)

#Lists Events
@router.get("/", response_model=List[EventResponse])
def list_events(
        db: Session = Depends(get_db)):
    """
            Returns the following information for all events registered in the DB:

            - **event_name**: returns event name
            - **event_description**: returns event description
            - **event_date**: returns event date
            - **ticket_link**: returns official ticket sales website link for the event
            - **event_location**: returns event location
            - **organizer_id**: returns event organizer ID
            - **artists**: returns a list of the artists participating in the event

    """
    return list_events_service(db)

#Get Event Artists
@router.get("/{event_id}/artists/{artist_id}")
def get_artist_event(event_id: int, artist_id: int, db: Session = Depends(get_db)):
    """
        Returns all artists from an event:

        - **event_id**: receives event ID

        Finds event by its ID and returns the list of artists participating and their information

    """
    return get_event_artists_service(event_id, artist_id, db)

#Add Artist to Event
@router.post("/{event_id}/artists/{artist_id}")
def add_artist_event(
        event_id: int,
        artist_id: int,
        db: Session = Depends(get_db)):
    """
            Adds more artists to the event:

            - **event_id**: receives event ID
            - **artist_id**: receives artist ID

            Receives event ID and artist ID, then adds the artist to the event

    """

    return add_artist_event_service(event_id, artist_id, db)

#Update Event
@router.patch("/{event_id}")
def update_event(
    event_id: int,
    updated_data: EventUpdate,
    db: Session = Depends(get_db)):
    """
        Updates event information:

        - **event_id**: receives event ID
        - **event_name**: returns event name
        - **event_description**: returns event description
        - **event_date**: returns event date
        - **ticket_link**: returns official ticket sales website link for the event
        - **event_location**: returns event location
        - **organizer_id**: returns event organizer ID
        - **artists**: returns a list of the artists participating in the event

        Finds an event by its ID and allows updating his data

    """
    return update_event_service(event_id, updated_data, db)

#Deletes event
@router.delete("/{event_id}")
def delete_event(
        event_id: int,
        db: Session = Depends(get_db)):

    """
        Deletes event:

        - **event_id**: receives event ID

        Finds event by its ID and deletes it from the DB

    """
    return delete_event_service(event_id, db)

#Remove Artist from Event
@router.delete("/{event_id}/artists/{artist_id}")
def remove_artist_event(
    event_id: int,
    artist_id: int,
    db: Session = Depends(get_db)
    ):

    """
        Updates event information:

        - **event_id**: recieves the event ID
        - **artist_id**: recieves the artist ID

        Finds the event by its ID, recieves the artist ID, and removes the artist from the event

    """
    return remove_artist_event_service(event_id, artist_id, db)