from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import create_user_service, list_users_service, add_genre_user_service, \
    get_user_genres_service, add_event_user_service, get_user_events_service, update_user_service, delete_user_service, \
    delete_genre_user_service

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

    return create_user_service(user, db)

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

    return list_users_service(db)

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

    return add_genre_user_service()

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

    return get_user_genres_service(user_id, db)

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

    return add_event_user_service(user_id, event_id, db)

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

    return get_user_events_service(user_id, db)

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

    return update_user_service(user_id, updated_data, db)

#Delete user
@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)):

    """
        Deletes user from the DB:

        - **user_id**: receives user ID

        Finds user by its ID and deletes it from the DB

    """

    return delete_user_service(user_id, db)

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

    return delete_genre_user_service(user_id, genere_id, db)