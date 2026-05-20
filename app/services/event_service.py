from datetime import date
from os.path import exists

from sqlalchemy.orm import Session

from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Event, Artist
from app.schemas import artist

#Create Event
def create_event_service(event_data, db: Session):

    if event_data.event_date < date.today():
        raise BadRequestException("Event date cannot be in the past")

    exists = db.query(Event).filter_by(event_name = event_data.event_name).first()

    if exists:
        raise ConflictException("Event already exists")

    db_event = Event(
        event_name = event_data.event_name,
        event_description = event_data.event_description,
        event_date = event_data.event_date,
        ticket_link=event_data.ticket_link,
        event_location=event_data.event_location,
        organizer_id=event_data.organizer_id
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    artist_objects = []

    for artist_name in event_data.artists:
        artist = db.query(Artist).filter(
            Artist.artist_name == artist_name
        ).first()

        if not artist:
            raise NotFoundException(f"Artist '{artist_name}' not found")

        artist_objects.append(artist)

    db_event.artists = artist_objects

    db.commit()

    return db_event

#List Event
def list_events_service(db: Session):
    return db.query(Event).all()

#Get Event Artists
def get_event_artists_service(event_id: int, db: Session):

    event = db.get(Event, event_id)

    if not event:
        raise NotFoundException("Event does not exist")

    return event.artists

#Add Artist to Event
def add_artist_event_service(event_id: int, artist_id: int, db: Session):
    event = db.get(Event, event_id)
    artist = db.get(Artist, artist_id)

    if not event or not artist:
        raise NotFoundException("Event or Artist does not exist")

    if artist in event.artists:
        raise ConflictException("Artist already in the event")

    event.artists.append(artist)

    db.commit()

    return {"message": "Artist added successfully!"}

#Update Event
def update_event_service(event_id: int, updated_data, db: Session):
    event = db.get(Event, event_id)

    if not event:
        raise NotFoundException("Event does not exist")

    updated_data = updated_data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(event, key, value)

        db.commit()
        db.refresh(event)

        return event

#Delete Event
def delete_event_service(event_id: int, db: Session):
    event = db.get(Event, event_id)

    if not event:
        raise NotFoundException("Event does not exist")

    event.artists.clear()

    db.delete(event)
    db.commit()

#Remove Artist from Event
def remove_artist_event_service(event_id: int, artist_id: int, db: Session):
    event = db.get(Event, event_id)
    artist = db.get(Artist, artist_id)

    if not event or not artist:
        raise NotFoundException("Event or Artist does not exist")

    if artist not in event.artist:
        raise NotFoundException("Artist not linked to this Event")
