from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.exceptions.ConflictException import ConflitException
from app.exceptions.NotFoundException import NotFoundException
from app.models.genre import Genre
from app.schemas.artist import ArtistResponse
from app.schemas.genre import GenreResponse, GenreCreate, GenreUpdate

router = APIRouter(prefix="/genres", tags=["genres"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Creates genre
@router.post("/", response_model=GenreResponse)
def create_genre(
        genre: GenreCreate,
        db: Session = Depends(get_db)):
    """
        Creates new genre in the DB:

        - **genre_name**: recieves genre name

    """

    #Finds event by genre name
    exists = db.query(Genre).filter_by(
        event_name = genre.genre_name
    ).first()

    #Verifies if genre already exists
    if exists:
        raise ConflitException("Genre already exists")

    db_genre = Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

#Lists all genres
@router.get("/", response_model=list[GenreResponse])
def list_genre(
        db: Session = Depends(get_db)):
    """
        Returns the following information for all genres registered in the DB:

        - **genre_name**: returns genre name
        - **genre_id**: returns genre id

    """
    genres = db.query(Genre).all()
    return genres

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

    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre not found")

    return genre.artists

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
    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre does not exist")

    update_genre = updated_data.model_dump(exclude_unset=True)

    for key, value in update_genre.items():
        setattr(genre, key, value)

    db.commit()
    db.refresh(genre)

    return genre

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
    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre does not exist")

    genre.users.clear()
    genre.artists.clear()

    db.delete(genre)
    db.commit()

    return {"message": "Genre deleted successfully!"}