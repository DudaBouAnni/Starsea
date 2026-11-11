"""Autorização OAuth do Spotify e consulta somente de leitura ao perfil e aos artistas."""

from urllib.parse import urlencode

import requests
from fastapi import HTTPException

from app.core.settings import settings

SPOTIFY_SCOPES = "user-read-email user-read-private user-top-read"
SPOTIFY_API = "https://api.spotify.com/v1"
REQUEST_TIMEOUT = (3.05, 10)


def _require_credentials():
    if not settings.SPOTIFY_CLIENT_ID.strip() or not settings.SPOTIFY_CLIENT_SECRET.strip():
        raise HTTPException(503, "Configure SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET no servidor.")


def _request_json(method: str, url: str, **kwargs) -> dict:
    try:
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
        if response.status_code in (401, 403):
            raise HTTPException(
                response.status_code,
                "Autorize novamente o Spotify e confira as permissões do aplicativo.",
            )
        if response.status_code == 429:
            retry = response.headers.get("Retry-After", "")
            headers = {"Retry-After": retry} if retry.isdigit() else None
            raise HTTPException(
                429,
                "Limite de consultas do Spotify atingido. Tente novamente depois.",
                headers=headers,
            )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict) or "error" in payload:
            raise ValueError("Invalid Spotify payload")
        return payload
    except requests.Timeout as exc:
        raise HTTPException(504, "O Spotify demorou a responder.") from exc
    except (requests.RequestException, ValueError) as exc:
        raise HTTPException(502, "Não foi possível consultar o Spotify.") from exc


def get_spotify_login_url(state: str | None = None):
    _require_credentials()
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": SPOTIFY_SCOPES,
    }
    if state is not None:
        params["state"] = state
    return "https://accounts.spotify.com/authorize?" + urlencode(params)


def get_access_token(code: str):
    _require_credentials()
    return _request_json(
        "POST",
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        },
    )


def get_spotify_user(access_token: str):
    return _request_json(
        "GET", f"{SPOTIFY_API}/me", headers={"Authorization": f"Bearer {access_token}"}
    )


def get_spotify_top_artists(access_token: str) -> list[dict]:
    data = _request_json(
        "GET",
        f"{SPOTIFY_API}/me/top/artists",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"time_range": "medium_term", "limit": 50},
    )
    items = data.get("items")
    if not isinstance(items, list):
        raise HTTPException(502, "O Spotify retornou uma lista de artistas inválida.")
    return items
