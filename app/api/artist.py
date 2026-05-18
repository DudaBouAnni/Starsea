from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.artist_service import create_artist_service, list_artists_service, \
    add_genre_artist_service, get_artist_events_service, update_artist_service, delete_artist_service, \
    remove_artist_genres_service
from app.schemas.artist import ArtistCreate, ArtistResponse, ArtistUpdate
from typing import List

from app.schemas.event import EventResponse

router = APIRouter(prefix="/artists", tags=["artists"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create Artist
@router.post("/", response_model=ArtistResponse)
def create_artist(
        artist: ArtistCreate,
        db: Session = Depends(get_db)):
    """
        Cria um novo artista no banco de dados:

        - **artist_name**: recebe nome do artista
        - **genres**: recebe nomes de gêneros existentes em lista
    """

    return create_artist_service(artist, db)

#Returns all artists
@router.get("/", response_model=List[ArtistResponse])
def list_artists(
        db: Session = Depends(get_db)):
    """
        Returns the following information for all artists registered in the DB:

        - **artist_name**: returns artist name
        - **artist_id**: returns artist ID
        - **genres**: returns artist's genre list

    """
    return list_artists_service(db)

#Adds genre to an artist
@router.post("/{artist_id}/genres/{genre_id}", response_model=ArtistResponse)
def add_genre_artist(
    artist_id: int,
    genre_id: int,
    db: Session = Depends(get_db)):

    """
       Adds new genre to an artist:

       - **artist_id**: receives artist ID
       - **genre_id**: receive genre ID

        Finds an artist by its ID and adds the selected genre to the artist's genre list
    """
    return add_genre_artist_service(artist_id, genre_id, db)

#Returns all events from an artist
@router.get("/{artist_id}/events", response_model=list[EventResponse])
def get_artist_events(
        artist_id: int,
        db: Session = Depends(get_db)):
    """
       Returns all events from an artist:

       - **artist_id**: receives artist ID

    """

    return get_artist_events_service(artist_id, db)

#Updates artist
@router.patch("/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: int,
    updated_data: ArtistUpdate,
    db: Session = Depends(get_db)
):
    """

       Updates artist information:

       - **artist_id**: recieves artist ID

       Finds the artist by its ID and allows updating its data

    """

    return update_artist_service(artist_id, updated_data, db)

#Deletes artist
@router.delete("/{artist_id}")
def delete_artist(
        artist_id: int,
        db: Session = Depends(get_db)):

    """
       Deletes artist from the DB

       - **artist_id**: receives artist ID

       Finds the artist by its ID and removes it from the DB
    """

    return delete_artist_service(artist_id, db)

#Deletes genre from an artist
@router.delete("/{artist_id}/genres/{genre_id}")
def remove_genre_artist(
    artist_id: int,
    genre_id: int,
    db: Session = Depends(get_db)
    ):
    """
       Removes genre from an artist:

       - **artist_id**: receives artist ID
       - **genre_id**: receives genre ID

       Finds the artist by its ID, then finds the artist's genre by its ID and removes it from the artist's genre list
    """

    return remove_artist_genres_service
