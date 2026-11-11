from sqlalchemy.orm import Session

from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Artist, Event, Organizer
from app.services.geo_service import local_today
from app.services.nearby_service import sync_event_notifications


# Cria um evento
def create_event_service(event_data, db: Session):

    if event_data.event_date < local_today():
        raise BadRequestException("Event date cannot be in the past")

    exists = db.query(Event).filter_by(event_name=event_data.event_name).first()

    if exists:
        raise ConflictException("Event already exists")

    if db.get(Organizer, event_data.organizer_id) is None:
        raise NotFoundException("Organizer not found")

    db_event = Event(
        event_name=event_data.event_name,
        event_description=event_data.event_description,
        event_date=event_data.event_date,
        ticket_link=event_data.ticket_link,
        event_location=event_data.event_location,
        organizer_id=event_data.organizer_id,
        latitude=event_data.latitude,
        longitude=event_data.longitude,
    )

    artist_objects = []

    for artist_name in event_data.artists:
        artist = db.query(Artist).filter(Artist.artist_name == artist_name).first()

        if not artist:
            raise NotFoundException(f"Artist '{artist_name}' not found")

        artist_objects.append(artist)

    db_event.artists = artist_objects
    db.add(db_event)
    sync_event_notifications(db_event, db)
    db.commit()
    db.refresh(db_event)

    return db_event


# Lista os eventos
def list_events_service(db: Session):
    return db.query(Event).all()


# Consulta os artistas do evento
def get_event_artists_service(event_id: int, db: Session):

    event = db.get(Event, event_id)

    if not event:
        raise NotFoundException("Event does not exist")

    return event.artists


# Adiciona um artista ao evento
def add_artist_event_service(event_id: int, artist_id: int, db: Session):
    event = db.get(Event, event_id)
    artist = db.get(Artist, artist_id)

    if not event or not artist:
        raise NotFoundException("Event or Artist does not exist")

    if artist in event.artists:
        raise ConflictException("Artist already in the event")

    event.artists.append(artist)
    sync_event_notifications(event, db)
    db.commit()

    return {"message": "Artist added successfully!"}


# Atualiza o evento
def update_event_service(event_id: int, updated_data, db: Session):
    event = db.get(Event, event_id)

    if not event:
        raise NotFoundException("Event does not exist")

    updated_data = updated_data.model_dump(exclude_unset=True)

    if any(
        value is None for key, value in updated_data.items() if key not in ("latitude", "longitude")
    ):
        raise BadRequestException("Os campos do evento não podem ser nulos, exceto as coordenadas.")
    if "event_date" in updated_data and updated_data["event_date"] < local_today():
        raise BadRequestException("Event date cannot be in the past")

    for key, value in updated_data.items():
        setattr(event, key, value)

    sync_event_notifications(event, db)
    db.commit()
    db.refresh(event)
    return event


# Exclui o evento
def delete_event_service(event_id: int, db: Session):
    event = db.get(Event, event_id)

    if not event:
        raise NotFoundException("Event does not exist")

    event.artists.clear()

    db.delete(event)
    db.commit()


# Remove um artista do evento
def remove_artist_event_service(event_id: int, artist_id: int, db: Session):
    event = db.get(Event, event_id)
    artist = db.get(Artist, artist_id)

    if not event or not artist:
        raise NotFoundException("Event or Artist does not exist")

    if artist not in event.artists:
        raise NotFoundException("Artist not linked to this Event")
    event.artists.remove(artist)
    sync_event_notifications(event, db)
    db.commit()
    return {"message": "Artist removed successfully!"}
