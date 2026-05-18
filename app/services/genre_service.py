from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflitException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Genre
from app.schemas.genre import GenreCreate, GenreUpdate


#Create Genre
def create_genre_service(genre: GenreCreate, db: Session):
    exists = db.query(Genre).filter_by(genre_name=genre.genre_name).first()

    if exists:
        raise ConflitException("Genre already exists")

    db_genre = Genre(genre_name=genre.genre_name)

    db.add(db_genre)

    db.commit()
    db.refresh(db_genre)

    return db_genre

#List Genres
def list_genre_service(db: Session):
    return db.query(Genre).all()

#Get Genre Artists
def get_genre_artists_service(genre_id: int, db: Session):
    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre does not exist")

    return genre.artists

#Update Genre
def update_genre_service(genre_id: int, updated_data: GenreUpdate, db: Session):
    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre does not exist")

    updated_data = updated_data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(genre, key, value)

    db.commit()
    db.refresh(genre)

    return genre

#Delete Genre
def delete_genre_service(genre_id: int, db: Session):
    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre does not exist")

    genre.users.clear()
    genre.artists.clear()

    db.delete(genre)

    db.commit()

    return {"message": "Genre deleted successfully!"}