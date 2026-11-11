import secrets
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.settings import settings
from app.schemas.music import SpotifyLoginResponse
from app.services.auth_service import spotify_callback_service
from app.services.spotify_service import get_spotify_login_url

router = APIRouter(prefix="/auth", tags=["auth"])
STATE_COOKIE = "starsea_spotify_state"


@router.get("/login")
def spotify_login(response: Response):
    """Inicia consentimento para perfil e artistas de maior afinidade do Spotify."""
    state = secrets.token_urlsafe(32)
    login_url = get_spotify_login_url(state)
    response.set_cookie(
        STATE_COOKIE,
        state,
        max_age=600,
        httponly=True,
        samesite="lax",
        secure=urlparse(settings.SPOTIFY_REDIRECT_URI).scheme == "https",
        path="/auth",
    )
    response.headers["Cache-Control"] = "no-store"
    return {"login_url": login_url}


@router.get("/callback", response_model=SpotifyLoginResponse)
def spotify_callback(
    request: Request,
    response: Response,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
):
    cookie = request.cookies.get(STATE_COOKIE)
    if not state or not cookie or not secrets.compare_digest(state.encode(), cookie.encode()):
        raise HTTPException(
            400, "Autorização inválida ou expirada. Inicie novamente em /auth/login."
        )
    if error or not code:
        raise HTTPException(
            400, "O acesso ao Spotify não foi autorizado. Inicie novamente em /auth/login."
        )
    result = spotify_callback_service(code, request.client.host if request.client else "", db)
    response.delete_cookie(STATE_COOKIE, path="/auth")
    response.headers["Cache-Control"] = "no-store"
    return result
