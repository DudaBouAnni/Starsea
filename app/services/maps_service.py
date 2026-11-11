from sqlalchemy.orm import Session

from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Event
from app.services.maps_links import location_maps_url


def event_map_url(event: Event) -> str:
    """Abre somente o local do show; a pessoa escolhe as rotas no próprio Google Maps."""
    url = location_maps_url(event.latitude, event.longitude, event.event_location)
    if url is None:
        raise BadRequestException(
            "O evento não possui coordenadas nem endereço para abrir no Maps."
        )
    return url


def get_event_map_url(event_id: int, db: Session) -> str:
    event = db.get(Event, event_id)
    if event is None:
        raise NotFoundException("Event not found")
    return event_map_url(event)
