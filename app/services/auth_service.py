from sqlalchemy.orm import Session

from app.exceptions.NotFoundException import NotFoundException
from app.models import User
from app.services.location_service import get_location_from_ip
from app.services.spotify_service import get_access_token, get_spotify_user


def spotify_callback_service(code: str, ip: str, db: Session):
    token_data = get_access_token(code)

    access_token = token_data.get("access_token")

    if not access_token:
        raise NotFoundException("Could not get access token")

    spotify_user = get_spotify_user(access_token)

    existing_user = db.query(User).filter(
        User.email == spotify_user.get("email")).first()

    if existing_user:
        existing_user.spotify_id = spotify_user.get("id")
        existing_user.country = spotify_user.get("country")
        existing_user.city = location.get("city")
        existing_user.state = location.get("region")


        if spotify_user.get("images"):
            existing_user.profile_image = spotify_user["images"][0]["url"]

        db.commit()
        db.refresh(existing_user)

        return {
            "message": "Login successful",
            "user": existing_user
        }

    profile_image = None

    if spotify_user.get("images"):
        profile_image = spotify_user["images"][0]["url"]

    new_user = User(
        username=spotify_user.get("display_name"),
        email=spotify_user.get("email"),
        spotify_id=spotify_user.get("id"),
        country=spotify_user.get("country"),
        profile_image=profile_image,
        city=location.get("city"),
        state=location.get("region")
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Account created successfully",
        "user": new_user
    }