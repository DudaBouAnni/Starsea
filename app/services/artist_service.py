from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.exceptions.ValidationException import ValidationException
from app.models import Artist, Genre
from app.services.nearby_service import sync_all_notifications


# Cria um artista
def create_artist_service(artist_data, db: Session):
    if (
        artist_data.spotify_id
        and db.query(Artist).filter_by(spotify_id=artist_data.spotify_id).first()
    ):
        raise ConflictException("Spotify artist already exists")
    db_artist = Artist(artist_name=artist_data.artist_name, spotify_id=artist_data.spotify_id)

    genre_objects = []

    for genre_name in artist_data.genres:
        genre = db.query(Genre).filter_by(genre_name=genre_name).first()

        if not genre:
            raise NotFoundException(f"Genre '{genre_name}' does not exist")

        genre_objects.append(genre)

    db_artist.genres = genre_objects

    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)

    return db_artist


# Lista os artistas
def list_artists_service(db: Session):
    artists = db.query(Artist).all()
    return artists


# Adiciona um gênero ao artista
def add_genre_artist_service(artist_id: int, genre_id: int, db: Session):

    artist = db.get(Artist, artist_id)
    genre = db.get(Genre, genre_id)

    if not artist or not genre:
        raise NotFoundException("Artist or Genre does not exist")

    if genre in artist.genres:
        raise ConflictException("Genre already linked to Artist")

    artist.genres.append(genre)
    sync_all_notifications(db)
    db.commit()
    db.refresh(artist)

    return artist


# Consulta os eventos do artista
def get_artist_events_service(artist_id: int, db: Session):
    artist = db.get(Artist, artist_id)

    if not artist:
        raise NotFoundException("Artist does not exist")

    return artist.events


# Atualiza o artista
def update_artist_service(artist_id: int, updated_data, db: Session):

    artist = db.get(Artist, artist_id)

    if not artist:
        raise NotFoundException("Artist does not exist")

    updated_data = updated_data.model_dump(exclude_unset=True)
    spotify_id = updated_data.get("spotify_id")
    if (
        spotify_id
        and db.query(Artist)
        .filter(Artist.spotify_id == spotify_id, Artist.artist_id != artist_id)
        .first()
    ):
        raise ConflictException("Spotify artist already exists")

    for key, value in updated_data.items():
        setattr(artist, key, value)

    db.commit()
    db.refresh(artist)

    return artist


# Exclui o artista
def delete_artist_service(artist_id: int, db: Session):
    artist = db.get(Artist, artist_id)

    if not artist:
        raise NotFoundException("Artist does not exist")

    artist.genres.clear()

    db.delete(artist)
    sync_all_notifications(db)
    db.commit()

    return {"message": "Arists deleted successfully!"}


# Remove um gênero do artista
def remove_artist_genres_service(artist_id: int, genre_id: int, db: Session):

    artist = db.get(Artist, artist_id)
    genre = db.get(Genre, genre_id)

    if not artist or not genre:
        raise NotFoundException("Artist or Genre does not exist")

    if genre not in artist.genres:
        raise ValidationException("Genre not linked to this Artist")

    artist.genres.remove(genre)
    sync_all_notifications(db)
    db.commit()

    return {"message": "Artist removed from Genre successfully!"}
