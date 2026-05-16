from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ConflictException import ConflitException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Event
from app.models.genre import Genre
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Creates user
@router.post("/", response_model=UserResponse)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db)):
    """
       Creates a user in the DB:

        - **username**: receives username
        - **email**: receives user email
        - **username_password**: receives user password

    """

    db_user = User(
    username = user.username,
    user_password = user.user_password,
    email = user.email,
    )

    db.add(db_user),
    db.commit(),
    db.refresh(db_user)

    return db_user

#Lists all users
@router.get("/", response_model=list[UserResponse])
def list_users(
        db: Session = Depends(get_db)):
    """
        Returns all users in the DB:

        - **user_id**: returns user ID
        - **username**: returns username
        - **email**: returns user email

    """

    users = db.query(User).all()
    return users

#Adds genre to user
@router.post("/{user_id}/genres/{genre_id}")
def add_genre_user(
        user_id: int,
        genre_id: int,
        db: Session = Depends(get_db)):
    """
        Adds new genre to the user:

        - **user_id**: receives user ID
        - **genre_id**: receives genre ID

        Finds the user by its ID, then finds the by its ID and adds it to the user's genre list
    """

    user = db.get(User, user_id)
    genre = db.get(Genre, genre_id)

    #Checks if user and/or genre exists in the DB
    if not user or not genre:
        raise NotFoundException("User or Genre does not exist")

    #Checks if user already has the genre linked
    if genre in user.genres:
        return ConflitException("Genre already exists")

    user.genres.append(genre)

    db.commit()

    return {"message": "Genre added successfully!"}

#Returns all genres from a user
@router.get("/{user_id}/genres")
def get_user_genres(
        user_id: int,
        db: Session = Depends(get_db)):
    """
        Returns all genres from a user:

        - **user_id**: receives user ID

        Finds user by its ID and returns the user's genre list.

    """

    user = db.get(User, user_id)

    if not user:
        raise NotFoundException("User not found")

    return user.genres

#Adds events to a user
@router.post("/{user_id}/events/{event_id}")
def add_event_user(
        user_id: int,
        event_id: int,
        db: Session = Depends(get_db)):
    """
        Adds new event to a user:

        - **user_id**: receives user ID
        - **event_id**: receives event ID

        Finds the user by its ID, then finds the event by its ID and adds it to the user's event list

    """
    user = db.get(User, user_id)
    event = db.get(Event, event_id)

    #Checks if user and/or event exists in the DB
    if not user or not event:
        raise NotFoundException("User or Event does not exist")

    #Checks if user already has this event linked
    if event in user.events:
        return {"message": "Event already added"}

    user.events.append(event)

    db.commit()

    return {"message": "Genre added successfully!"}

#Returns all events from a user
@router.get("/{user_id}/events")
def get_user_events(
        user_id: int,
        db: Session = Depends(get_db)):

    """
        Returns all events from a user:

        - **user_id**: receives user ID

        Finds user by its ID and returns the user's event list

    """

    user = db.get(User, user_id)

    if not user:
        raise NotFoundException("User not found")

    return user.events

#Updates user
@router.patch("/{user_id}")
def update_user(
    user_id: int,
    updated_data: UserUpdate,
    db: Session = Depends(get_db)):

    """
        Updates user:

        - **user_id**: receives user ID

        Finds user by its id and allows updating its data

    """

    user = db.get(User, user_id)

    if not user:
        raise NotFoundException("User does not exist")

    update_user = updated_data.model_dump(exclude_unset=True)

    for key, value in update_user.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

#Deletes user
@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)):

    """
        Deletes user from the DB:

        - **user_id**: receives user ID

        Finds user by its ID and deletes it from the DB

    """

    user = db.get(User, user_id)

    if not user:
        raise NotFoundException("User does not exist")

    user.genres.clear()
    user.events.clear()

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully!"}

#Deletes a genre from a user
@router.delete("/{user_id}/genres/{genere_id}")
def delete_genre_user(
        user_id: int,
        genere_id: int,
        db: Session = Depends(get_db)):

    """
        Deleta um gênero de um usuário:

        - **user_id**: receives user ID
        - **genre_id**: receives genre ID

        Finds user by its ID, finds genre by its ID, and removes it from the user's genre list

    """

    user = db.get(User, user_id)
    genre = db.get(Genre, genere_id)

    #Checks if user and/or genre exists in the DB
    if not user or not genre:
        raise NotFoundException("User or Genre does not exist")

    #Checks if genre is in user's genre list
    if genre not in user.genres:
        raise BadRequestException("Genre not linked")

    user.genres.remove(genre)

    db.commit()

    return {"message": "Genre unfavorited successfully!"}