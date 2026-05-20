from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.exceptions.ValidationException import ValidationException
from app.models import Artist, Genre


#Create Artist
def create_artist_service(artist_data, db: Session):
    db_artist = Artist(artist_name = artist_data.artist_name)

    genre_objects = []

    for genre_name in artist_data.genres:
        genre = db.query(Genre).filter_by(
            genre_name = genre_name
        ).first()

        if not genre:
            raise NotFoundException(
                f"Genre '{genre_name}' does not exist"
            )

        genre_objects.append(genre)

    db_artist.genres = genre_objects

    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)

    return db_artist

#List Artists
def list_artists_service(db: Session):
    artists = db.query(Artist).all()

#Add Genre to Artist
def add_genre_artist_service(artist_id: int, genre_id: int, db: Session):

    artist = db.get(Artist, artist_id)
    genre = db.get(Genre, genre_id)

    if not artist or not genre:
        raise NotFoundException("Artist or Genre does not exist")

    if genre in artist.genres:
        raise ConflictException("Genre already linked to Artist")

    artist.genres.append(genre)

    db.commit()
    db.refresh(artist)

    return {"message": "Genre added successfully!"}

#Get Artist Events
def get_artist_events_service(artist_id: int, db: Session):
    artist = db.get(Artist, artist_id)

    if not artist:
        raise NotFoundException("Artist does not exist")

    return artist.events

#Update Artist
def update_artist_service(artist_id: int, updated_data, db: Session):

    artist = db.get(Artist, artist_id)

    if not artist:
        raise NotFoundException("Artist does not exist")

    updated_data = updated_data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(artist, key, value)

    db.commit()
    db.refresh(artist)

    return artist

#Delete Artist
def delete_artist_service(artist_id: int, db: Session):
    artist = db.get(Artist, artist_id)

    if not artist:
        raise NotFoundException("Artist does not exist")

    artist.genres.clear()

    db.delete(artist)
    db.commit()

    return {"message": "Arists deleted successfully!"}

#Remove Artist Genre
def remove_artist_genres_service(artist_id: int, genre_id: int, db: Session):

    artist = db.get(Artist, artist_id)
    genre = db.get(Genre, genre_id)

    if not artist or not genre:
        raise NotFoundException("Artist or Genre does not exist")

    if genre not in artist.genres:
        raise ValidationException("Genre not linked to this Artist")

    artist.genres.remove(genre)

    db.commit()

    return {"message": "Artist removed from Genre successfully!"}