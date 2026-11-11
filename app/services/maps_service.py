import math
import os
from urllib.parse import urlencode

import requests
from sqlalchemy.orm import Session

from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Event, User
from app.schemas.nearby import EventRoutes, RouteOption, TravelMode
from app.services.geo_service import distance_km, has_coordinates, local_today
from app.services.nearby_service import get_user, require_user_location

ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
GOOGLE_MODES = {"driving": "DRIVE", "walking": "WALK", "bicycling": "BICYCLE", "transit": "TRANSIT"}


def _waypoint(entity):
    """Converte as coordenadas salvas para o formato de requisição do Google Routes."""
    return {"location": {"latLng": {"latitude": entity.latitude, "longitude": entity.longitude}}}


def _route_estimates(route):
    """Converte as estimativas do Google para quilômetros e minutos."""
    # O JSON do Protobuf pode omitir campos de distância e duração com valor zero.
    distance = float(route.get("distanceMeters", 0)) / 1000
    duration_text = route.get("duration", "0s")
    if not isinstance(duration_text, str) or not duration_text.endswith("s"):
        raise ValueError("Invalid duration")
    duration = float(duration_text[:-1]) / 60
    if not all(math.isfinite(value) and value >= 0 for value in (distance, duration)):
        raise ValueError("Invalid route estimate")
    return distance, duration


def maps_url(user: User, event: Event, mode: TravelMode = TravelMode.driving) -> str:
    return "https://www.google.com/maps/dir/?" + urlencode(
        {
            "api": 1,
            "origin": f"{user.latitude},{user.longitude}",
            "destination": f"{event.latitude},{event.longitude}",
            "travelmode": TravelMode(mode).value,
        }
    )


def route_option(user: User, event: Event, mode: TravelMode, limit_km: float) -> RouteOption:
    option = RouteOption(
        travel_mode=mode,
        available=False,
        maps_url=maps_url(user, event, mode),
        status="maps_not_configured",
    )
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    if not api_key:
        return option

    try:
        response = requests.post(
            ROUTES_URL,
            headers={
                "X-Goog-Api-Key": api_key,
                "X-Goog-FieldMask": "routes.distanceMeters,routes.duration",
            },
            json={
                "origin": _waypoint(user),
                "destination": _waypoint(event),
                "travelMode": GOOGLE_MODES[mode.value],
                "languageCode": "pt-BR",
                "units": "METRIC",
            },
            timeout=(3.05, 10),
        )
        response.raise_for_status()
        data = response.json()
        routes = data.get("routes", [])
        if not routes:
            option.status = "no_route"
            return option
        distance, duration = _route_estimates(routes[0])
        option.available = True
        option.distance_km = round(distance, 2)
        option.duration_minutes = round(duration, 1)
        option.within_distance_limit = distance <= limit_km
        option.status = "ok"
    except requests.Timeout:
        option.status = "provider_timeout"
    except requests.RequestException:
        option.status = "provider_error"
    except (ValueError, TypeError, KeyError, AttributeError, IndexError):
        option.status = "invalid_provider_response"
    return option


def get_event_routes(
    user_id: int,
    event_id: int,
    db: Session,
    modes: list[TravelMode] | None = None,
    max_distance_km: float | None = None,
) -> EventRoutes:
    user = get_user(user_id, db)
    require_user_location(user)
    event = db.get(Event, event_id)
    if event is None:
        raise NotFoundException("Event not found")
    if not has_coordinates(event):
        raise BadRequestException("O evento ainda não possui coordenadas.")
    if event.event_date is None or event.event_date < local_today():
        raise BadRequestException("O evento já passou ou não possui data.")
    limit_km = max_distance_km if max_distance_km is not None else user.notification_radius_km
    selected = list(dict.fromkeys(modes or list(TravelMode)))
    return EventRoutes(
        event_id=event.event_id,
        event_date=event.event_date,
        straight_line_distance_km=round(
            distance_km(user.latitude, user.longitude, event.latitude, event.longitude), 2
        ),
        distance_limit_km=limit_km,
        routes=[route_option(user, event, mode, limit_km) for mode in selected],
    )
