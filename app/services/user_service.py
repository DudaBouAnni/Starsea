from sqlalchemy.orm import Session
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ConflictException import ConflitException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Event
from app.models.genre import Genre
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

#Create User
def create_user_service(user: UserCreate, db: Session):
    exists = db.query(User).filter(User.email == user.email).first()

    if exists:
        raise ConflitException("Email already registered")

    db_user = User(
        username = user.username,
        email = user.email,
        user_password=user.user_password
    )

    db.add(db_user),
    db.commit(),
    db.refresh(db_user)

    return db_user

#Lists Users
def list_users_service(db: Session):
    return db.query(User).all()

#Add Genre to User
def add_genre_user_service(user_id: int, genre_id: int, db: Session):
    user = db.get(User, user_id)
    genre = db.get(Genre, genre_id)

    if not user or not genre:
        raise NotFoundException("User or Genre does not exist")

    if genre in user.genres:
        raise ConflitException("Genre already exists")

    user.genres.append(genre)

    db.commit()

    return {"message": "Genre added successfully!"}

#Get User Genres
def get_user_genres_service(user_id: int, db: Session):
    user = db.get(User, user_id)

    if not user:
        raise NotFoundException("User not found")

    return user.genres

#Add Event to User
def add_event_user_service(user_id: int, event_id: int, db: Session):
    user = db.get(User, user_id)
    event = db.get(Event, event_id)

    if not user or not event:
        raise NotFoundException("User or Event does not exist")

    if event in user.events:
        raise ConflitException("Event already linked")

    user.events.append(event)

    db.commit()

    return {"message": "Event added successfully!"}

#Get User Events
def get_user_events_service(user_id: int, db: Session):
    user = db.get(User, user_id)

    if not user:
        raise NotFoundException("User not found")

    return user.events

#Update User
def update_user_service(user_id: int, updated_data: UserUpdate, db: Session):
    user = db.get(User, user_id)

    if not user:
        raise NotFoundException("User does not exist")

    update_user = updated_data.model_dump(exclude_unset=True)

    for key, value in update_user.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

#Delete User
def delete_user_service(user_id: int, db: Session):
    user = db.get(User, user_id)

    if not user:
        raise NotFoundException("User does not exist")

    user.genres.clear()
    user.events.clear()

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully!"}

#Delete User Genre
def delete_genre_user_service(user_id: int, genere_id: int, db: Session):
    user = db.get(User, user_id)
    genre = db.get(Genre, genere_id)

    if not user or not genre:
        raise NotFoundException("User or Genre does not exist")

    if genre not in user.genres:
        raise BadRequestException("Genre not linked")

    user.genres.remove(genre)

    db.commit()

    return {"message": "Genre unfavorited successfully!"}