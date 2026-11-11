"""Importa o perfil autorizado do Spotify e suas preferências em uma única transação."""

from ipaddress import ip_address

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflictException
from app.models import User
from app.schemas.user import UserResponse
from app.services.location_service import get_location_from_ip
from app.services.music_service import import_spotify_artists
from app.services.spotify_service import get_access_token, get_spotify_top_artists, get_spotify_user


def _optional_location(ip: str) -> dict:
    try:
        if not ip_address(ip).is_global:
            return {}
        location = get_location_from_ip(ip)
        return location if isinstance(location, dict) and location.get("success") is True else {}
    except (ValueError, requests.RequestException):
        return {}


def spotify_callback_service(code: str, ip: str, db: Session):
    token_data = get_access_token(code)
    access_token = token_data.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise HTTPException(502, "Não foi possível obter autorização do Spotify.")
    profile = get_spotify_user(access_token)
    top_artists = get_spotify_top_artists(access_token)
    spotify_id, email = profile.get("id"), profile.get("email")
    if not isinstance(spotify_id, str) or not spotify_id or not isinstance(email, str) or not email:
        raise HTTPException(502, "O Spotify não retornou identificação e e-mail do usuário.")

    user = db.query(User).filter_by(spotify_id=spotify_id).first()
    if user is None:
        user = db.query(User).filter_by(email=email).first()
        if user is not None and user.spotify_id not in (None, spotify_id):
            raise ConflictException("Este e-mail já está associado a outra conta Spotify.")
    created = user is None
    if created:
        user = User(username=profile.get("display_name") or spotify_id, email=email)
        db.add(user)
    user.spotify_id = spotify_id
    user.country = profile.get("country")
    images = profile.get("images") or []
    if images and isinstance(images[0], dict):
        user.profile_image = images[0].get("url")
    location = _optional_location(ip)
    if location:
        user.city = location.get("city")
        user.state = location.get("region")

    try:
        imported = import_spotify_artists(user, top_artists, db)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise
    # Retorna apenas os dados públicos, sem a coluna de senha do modelo nem os tokens OAuth.
    return {
        "message": "Account created successfully" if created else "Login successful",
        "user": UserResponse.model_validate(user),
        "imported_artists": imported,
    }
