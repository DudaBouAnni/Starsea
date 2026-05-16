from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import SessionLocal
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ConflictException import ConflitException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Artist, event
from app.models.event import Event
from app.schemas.event import EventResponse, EventCreate, EventUpdate

router = APIRouter(prefix="/events", tags=["events"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Creates event
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

    #Checks if event date is not in the past
    if event.event_date < date.today():
        raise BadRequestException("Event date cannot be in the past")

    #Finds event by name
    exists = db.query(Event).filter_by(
        event_name = event.event_name
    ).first()

    #Checks if event already exists in the DB
    if exists:
        raise ConflitException("Event already exists")

    db_event = Event(
        event_name=event.event_name,
        event_description=event.event_description,
        event_date= event.event_date,
        ticket_link=event.ticket_link,
        event_location=event.event_location,
        organizer_id=event.organizer_id
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    #Checks if the artist is in any event
    artist_objetcs = []

    for artist_name in event.artists:
        artist = db.query(Artist).filter(
            Artist.artist_name == artist_name
        ).first()


        if not artist:
            raise NotFoundException("Artist '{artist_name}' does not exist")

        artist_objetcs.append(artist)

    db_event.artists = artist_objetcs

    db.commit()

    return db_event

#Lists all events
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
    events = db.query(Event).all()
    return events

#Returns all artists from an event
@router.get("/{event_id}/artists/{artist_id}")
def get_artist_event(
        event_id: int,
        db: Session = Depends(get_db)):
    """
        Returns all artists from an event:

        - **event_id**: receives event ID

        Finds event by its ID and returns the list of artists participating and their information

    """

    event = db.get(Event, event_id)
    return event.artists

#Adds more artists to the event
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

    event = db.get(Event, event_id)
    artist = db.get(Artist, artist_id)

    #Checks if artist and/or event exists in the DB
    if not event or not artist:
        raise ConflitException("Event or artist does not exist")

    #Checks for duplicate artist
    if artist in event.artists:
        raise ConflitException("Artist already in event")

    event.artists.append(artist)

    db.commit()

    return {"message": "Artist added successfully!"}

#Updates event
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

    event = db.get(Event, event_id)

    #Checks if event exists in the DB
    if not event:
        raise NotFoundException("Event does not exist")

    update_event = updated_data.model_dump(exclude_unset=True)

    for key, value in update_event.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    return event

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

    event = db.get(Event, event_id)

    if not event:
        raise NotFoundException("Event does not exist")

    event.artists.clear()

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully!"}

#Deletes an artist from an event
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

    event = db.get(Event, event_id)
    artist = db.get(Artist, artist_id)

    #Checks if the event and/or artist exists in the DB

    if not event or not artist:
        NotFoundException("Event or Artist does not exist")

    #

    if artist not in event.artists:
        raise NotFoundException("Artist not linked to this event")

    event.artists.remove(artist)

    db.commit()

    return {"message": "Artist removed from event"}