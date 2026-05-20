from fastapi import APIRouter
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
def spotify_callback(code: str, db: Session = Depends(get_db)):
    return spotify_callback_service(code, db)