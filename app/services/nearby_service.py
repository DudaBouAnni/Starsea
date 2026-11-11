from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Event, Notification, User
from app.schemas.location import (
    NotificationPreferences,
    NotificationPreferencesUpdate,
    UserLocationUpdate,
)
from app.services.geo_service import distance_km, has_coordinates, local_today
from app.services.music_match_service import (
    matched_artists,
    matched_genres,
    matches_music_preferences,
    music_event_filter,
)


def get_user(user_id: int, db: Session) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise NotFoundException("User not found")
    return user


def require_user_location(user: User) -> None:
    if not has_coordinates(user):
        raise BadRequestException("Defina a latitude e longitude do usuário primeiro.")


def update_user_location(
    user_id: int, location: UserLocationUpdate, db: Session
) -> UserLocationUpdate:
    user = get_user(user_id, db)
    user.latitude, user.longitude = location.latitude, location.longitude
    sync_user_notifications(user, db)
    db.commit()
    return location


def clear_user_location(user_id: int, db: Session) -> dict[str, str]:
    user = get_user(user_id, db)
    user.latitude = user.longitude = None
    sync_user_notifications(user, db)
    db.commit()
    return {"message": "Localização e avisos de proximidade removidos."}


def get_user_notification_preferences(user_id: int, db: Session) -> NotificationPreferences:
    user = get_user(user_id, db)
    return NotificationPreferences(
        notification_radius_km=user.notification_radius_km,
        nearby_notifications_enabled=user.nearby_notifications_enabled,
        personalized_notifications_only=user.personalized_notifications_only,
    )


def update_user_notification_preferences(
    user_id: int, preferences: NotificationPreferencesUpdate, db: Session
) -> NotificationPreferences:
    user = get_user(user_id, db)
    for key, value in preferences.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    sync_user_notifications(user, db)
    db.commit()
    return get_user_notification_preferences(user_id, db)


def refresh_user_notifications(user_id: int, db: Session) -> dict[str, int]:
    created = sync_user_notifications(get_user(user_id, db), db)
    db.commit()
    return {"created": created}


def nearby_events(user: User, db: Session, radius_km: float) -> list[tuple[Event, float]]:
    require_user_location(user)
    events = (
        db.query(Event)
        .filter(
            Event.event_date >= local_today(),
            Event.latitude.is_not(None),
            Event.longitude.is_not(None),
        )
        .all()
    )
    matches = []
    for event in events:
        distance = distance_km(user.latitude, user.longitude, event.latitude, event.longitude)
        if distance <= radius_km:
            matches.append((event, distance))
    return sorted(matches, key=lambda item: (item[1], item[0].event_id))


def sync_user_notifications(user: User, db: Session) -> int:
    """Sincroniza os avisos sem confirmar a transação de quem chamou a função."""
    db.flush()
    matches = (
        [
            (event, distance)
            for event, distance in nearby_events(user, db, user.notification_radius_km)
            if matches_music_preferences(user, event)
        ]
        if (user.nearby_notifications_enabled and has_coordinates(user))
        else []
    )
    existing = {
        item.event_id: item for item in db.query(Notification).filter_by(user_id=user.user_id).all()
    }
    eligible = {event.event_id for event, _ in matches}
    for event_id, notification in existing.items():
        if event_id not in eligible:
            db.delete(notification)
    created = 0
    for event, distance in matches:
        created += _save_notification(user, event, distance, existing.get(event.event_id), db)
    return created


def sync_all_notifications(db: Session) -> None:
    """Atualiza os avisos afetados pelo catálogo, preservando os dados importados e a leitura."""
    db.flush()
    db.expire_all()
    for user in db.query(User).all():
        sync_user_notifications(user, db)


def _save_notification(
    user: User, event: Event, distance: float, existing: Notification | None, db: Session
) -> int:
    message = f"{event.event_name} em {event.event_date:%d/%m/%Y}, a {distance:.1f} km de você (em linha reta)."
    favorites = matched_artists(user, event)
    if favorites:
        # Respeita o limite da coluna mesmo quando um festival possui muitos artistas.
        message = f"{', '.join(favorites)}: {message}"[:500]
    else:
        genres = matched_genres(user, event)
        if genres:
            message = f"Porque você gosta de {', '.join(genres)}: {message}"[:500]
    if existing is not None:
        existing.message = message
        existing.distance_km = distance
        return 0
    try:
        # Uma sincronização concorrente não deve duplicar avisos nem desfazer o evento ou usuário.
        with db.begin_nested():
            db.add(
                Notification(
                    user_id=user.user_id,
                    event_id=event.event_id,
                    message=message,
                    distance_km=distance,
                )
            )
            db.flush()
        return 1
    except IntegrityError:
        if (
            not db.query(Notification)
            .filter_by(user_id=user.user_id, event_id=event.event_id)
            .first()
        ):
            raise
        return 0


def sync_event_notifications(event: Event, db: Session) -> None:
    """Executada ao criar ou editar um show, inclusive quando a data ou o local mudam."""
    db.flush()
    existing = {
        item.user_id: item
        for item in db.query(Notification).filter_by(event_id=event.event_id).all()
    }
    upcoming = event.event_date is not None and event.event_date >= local_today()
    for user in db.query(User).all():
        distance = None
        if (
            upcoming
            and has_coordinates(event)
            and has_coordinates(user)
            and user.nearby_notifications_enabled
        ):
            distance = distance_km(user.latitude, user.longitude, event.latitude, event.longitude)
        if (
            distance is not None
            and distance <= user.notification_radius_km
            and matches_music_preferences(user, event)
        ):
            _save_notification(user, event, distance, existing.get(user.user_id), db)
        elif user.user_id in existing:
            db.delete(existing[user.user_id])


def list_notifications(
    user_id: int, db: Session, unread_only: bool = False, offset: int = 0, limit: int = 50
) -> list[Notification]:
    user = get_user(user_id, db)
    if not user.nearby_notifications_enabled or not has_coordinates(user):
        return []
    query = (
        db.query(Notification)
        .join(Event)
        .filter(
            Notification.user_id == user_id,
            Event.event_date >= local_today(),
        )
    )
    if unread_only:
        query = query.filter(Notification.is_read.is_(False))
    if user.personalized_notifications_only:
        query = query.filter(music_event_filter(user))
    return (
        query.order_by(Notification.created_at.desc(), Notification.notification_id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def mark_notification_read(user_id: int, notification_id: int, db: Session) -> Notification:
    get_user(user_id, db)
    notification = (
        db.query(Notification).filter_by(user_id=user_id, notification_id=notification_id).first()
    )
    if notification is None:
        raise NotFoundException("Notification not found")
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification
