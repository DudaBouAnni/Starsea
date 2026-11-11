from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.location import (
    NotificationPreferences,
    NotificationPreferencesUpdate,
    UserLocationUpdate,
)
from app.schemas.nearby import NearbyEvent, NotificationResponse
from app.services.maps_service import event_map_url
from app.services.nearby_service import (
    clear_user_location,
    get_user,
    get_user_notification_preferences,
    list_notifications,
    mark_notification_read,
    nearby_events,
    refresh_user_notifications,
    update_user_location,
    update_user_notification_preferences,
)

router = APIRouter(prefix="/users", tags=["nearby shows"])


@router.put("/{user_id}/location", response_model=UserLocationUpdate)
def update_location(user_id: int, location: UserLocationUpdate, db: Session = Depends(get_db)):
    """Recebe coordenadas do dispositivo ou de um ponto escolhido pelo usuário e atualiza os avisos."""
    return update_user_location(user_id, location, db)


@router.delete("/{user_id}/location")
def clear_location(user_id: int, db: Session = Depends(get_db)):
    return clear_user_location(user_id, db)


@router.get("/{user_id}/notification-preferences", response_model=NotificationPreferences)
def get_preferences(user_id: int, db: Session = Depends(get_db)):
    return get_user_notification_preferences(user_id, db)


@router.patch("/{user_id}/notification-preferences", response_model=NotificationPreferences)
def update_preferences(
    user_id: int, preferences: NotificationPreferencesUpdate, db: Session = Depends(get_db)
):
    return update_user_notification_preferences(user_id, preferences, db)


@router.get("/{user_id}/nearby-events", response_model=list[NearbyEvent])
def get_nearby_events(
    user_id: int,
    radius_km: float | None = Query(None, gt=0, le=1000, allow_inf_nan=False),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Shows de hoje em diante, ordenados por distância em linha reta. Não chama a API paga."""
    user = get_user(user_id, db)
    matches = nearby_events(
        user, db, radius_km if radius_km is not None else user.notification_radius_km
    )
    return [
        NearbyEvent(event=event, distance_km=round(distance, 2), maps_url=event_map_url(event))
        for event, distance in matches[offset : offset + limit]
    ]


@router.get("/{user_id}/notifications", response_model=list[NotificationResponse])
def get_notifications(
    user_id: int,
    unread_only: bool = False,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return list_notifications(user_id, db, unread_only, offset, limit)


@router.post("/{user_id}/notifications/refresh")
def refresh_notifications(user_id: int, db: Session = Depends(get_db)):
    """Sincroniza também shows importados diretamente no banco, sem duplicar os avisos existentes."""
    return refresh_user_notifications(user_id, db)


@router.patch(
    "/{user_id}/notifications/{notification_id}/read", response_model=NotificationResponse
)
def read_notification(user_id: int, notification_id: int, db: Session = Depends(get_db)):
    return mark_notification_read(user_id, notification_id, db)
