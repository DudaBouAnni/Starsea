from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.exceptions import ValidationException
from app.exceptions.NotFoundException import NotFoundException
from app.models.artist import Artist
from app.models.genre import Genre
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

#Creates new artist
@router.post("/", response_model=ArtistResponse)
def create_artist(
        artist: ArtistCreate,
        db: Session = Depends(get_db)):
    """
        Cria um novo artista no banco de dados:

        - **artist_name**: recebe nome do artista
        - **genres**: recebe nomes de gêneros existentes em lista
    """
    db_artist = Artist(
        artist_name=artist.artist_name
   )

    #Defines genre object
    genre_objects = []

    #Checks if genre exists in the DB
    for genre_name in artist.genres:
        genre = db.query(Genre).filter_by(
            genre_name = genre_name
        ).first()

        if not genre:
            raise NotFoundException(f"Genre '{genre_name}' does not exist.")

        genre_objects.append(genre)

    db_artist.genres = genre_objects

    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)

    return db_artist

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
    return db.query(Artist).all()

#Adds genre to an artist
@router.post("/{artist_id}/genres/{genre_id}", response_model=ArtistResponse)
def add_genre_to_artist(
    artist_id: int,
    genre_id: int,
    db: Session = Depends(get_db)):

    """
       Adds new genre to an artist:

       - **artist_id**: receives artist ID
       - **genre_id**: receive genre ID

        Finds an artist by its ID and adds the selected genre to the artist's genre list
    """

    artist = db.get(Artist, artist_id)
    genre = db.get(Genre, genre_id)

    #Checks if artist or genre exists in the DB
    if not artist or not genre:
        raise NotFoundException("Artist does not exist")

    artist.genres.append(genre)

    db.commit()

#Returns all events from an artist
@router.get("/{artist_id}/events", response_model=list[EventResponse])
def get_artist_events(
        artist_id: int,
        db: Session = Depends(get_db)):
    """
       Returns all events from an artist:

       - **artist_id**: receives artist ID

    """

    artist = db.get(Artist, artist_id)

    if not artist:
        raise NotFoundException("Artist not found")

    return artist.events

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

    artist = db.get(Artist, artist_id)

    #Checks if artist exists in the DB
    if not artist:
        raise NotFoundException("Artist does not exist")

    update_artist = updated_data.model_dump(exclude_unset=True)

    for key, value in update_artist.items():
        setattr(artist, key, value)

    db.commit()
    db.refresh(artist)

    return artist

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

    artist = db.get(Artist, artist_id)

    #Checks if artist exists in the DB
    if not artist:
        raise NotFoundException("Artist does not exist")

    artist.genres.clear()

    db.delete(artist)
    db.commit()

    return {"message": "Artist deleted successfully!"}

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

    artist = db.get(Artist, artist_id)
    genre = db.get(Genre, genre_id)

    #Checks if artist and/or genre exists in the DB
    if not artist or not genre:
        raise NotFoundException("Artist or Genre does not exist")

    #Checks if the genre is linked to the artist
    if genre not in artist.genres:
        raise ValidationException("Genre not linked to this artist")

    artist.genres.remove(genre)

    db.commit()

    return {"message": "Genre removed from artist successfully!"}
