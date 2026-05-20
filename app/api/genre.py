from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models.genre import Genre
from app.schemas.artist import ArtistResponse
from app.schemas.genre import GenreResponse, GenreCreate, GenreUpdate
from app.services.genre_service import delete_genre_service, update_genre_service, get_genre_artists_service, \
    list_genre_service

router = APIRouter(prefix="/genres", tags=["genres"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create Genre
@router.post("/", response_model=GenreResponse)
def create_genre(
        genre: GenreCreate,
        db: Session = Depends(get_db)):
    """
        Creates new genre in the DB:

        - **genre_name**: recieves genre name

    """

    return create_genre

#List Genres
@router.get("/", response_model=list[GenreResponse])
def list_genre(
        db: Session = Depends(get_db)):
    """
        Returns the following information for all genres registered in the DB:

        - **genre_name**: returns genre name
        - **genre_id**: returns genre id

    """
    return list_genre_service()

#Lists all artists in a genre
@router.get("/{genre_id}/artists", response_model=list[ArtistResponse])
def get_genre_artists(
        genre_id: int,
        db: Session = Depends(get_db)):
    """
        Returns all artists from a genre:

        - **genre_id**: recieves id do gênero

        Finds genre by its ID and returns the list of artists and their information
    """

    return get_genre_artists_service(genre_id, db)

#Updates genre
@router.patch("/{genre_id}")
def update_genre(
    genre_id: int,
    updated_data: GenreUpdate,
    db: Session = Depends(get_db)):
    """
        Updates genre information:

        - **genre_id**: recieves genre ID

        Finds the genre by its ID and allows updating its data

    """

    return update_genre_service(genre_id, updated_data, db)

#Deletes genre
@router.delete("/{genre_id}")
def delete_genre(
        genre_id: int,
        db: Session = Depends(get_db)):
    """
        Deletes genre from the DB:

        - **genre_id**: receive genre ID

        Finds the genre by its ID and allows deletes it from the DB

    """

    return delete_genre_service(genre_id, db)