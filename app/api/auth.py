from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api.user import get_db
from app.services.auth_service import spotify_callback_service
from app.services.spotify_service import get_spotify_login_url, get_access_token, get_spotify_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
def spotify_login():
    return {
        "login_url": get_spotify_login_url()
    }

@router.get("/callback")
def spotify_callback(code: str, request: Request, db: Session = Depends(get_db)):

    ip = request.client.host

    print("ip recebido: ",ip)

    return spotify_callback_service(code, ip, db)