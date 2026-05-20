from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models import User
from app.services.spotify_service import get_access_token, get_spotify_user


def spotify_callback_service(code: str, db: Session):
    token_data = get_access_token(code)

    access_token = token_data.get("access_token")

    if not access_token:
        raise NotFoundException("Could not get access token")

    spotify_user = get_spotify_user(access_token)

    existing_user = db.query(User).filter(
        User.email == spotify_user.get("email")).first()

    if existing_user:
        raise ConflictException("There is already a user with this email")

    profile_image = None

    if spotify_user.get("images"):
        profile_image = spotify_user["images"][0]["url"]

    new_user = User(
        username=spotify_user.get("display_name"),
        email=spotify_user.get("email"),
        spotify_id=spotify_user.get("id"),
        country=spotify_user.get("country"),
        profile_image=profile_image,
        user_password=""
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Account created successfully",
        "user": new_user
    }