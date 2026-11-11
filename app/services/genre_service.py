from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from app.services.nearby_service import sync_all_notifications


# Cria um gênero
def create_genre_service(genre: GenreCreate, db: Session):
    exists = db.query(Genre).filter_by(genre_name=genre.genre_name).first()

    if exists:
        raise ConflictException("Genre already exists")

    db_genre = Genre(genre_name=genre.genre_name)

    db.add(db_genre)

    db.commit()
    db.refresh(db_genre)

    return db_genre


# Lista os gêneros
def list_genre_service(db: Session):
    return db.query(Genre).all()


# Consulta os artistas do gênero
def get_genre_artists_service(genre_id: int, db: Session):
    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre does not exist")

    return genre.artists


# Atualiza o gênero
def update_genre_service(genre_id: int, updated_data: GenreUpdate, db: Session):
    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre does not exist")

    updated_data = updated_data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(genre, key, value)
    sync_all_notifications(db)
    db.commit()
    db.refresh(genre)

    return genre


# Exclui o gênero
def delete_genre_service(genre_id: int, db: Session):
    genre = db.get(Genre, genre_id)

    if not genre:
        raise NotFoundException("Genre does not exist")

    genre.users.clear()
    genre.artists.clear()

    db.delete(genre)
    sync_all_notifications(db)
    db.commit()

    return {"message": "Genre deleted successfully!"}
