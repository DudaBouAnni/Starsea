from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
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

#Insere genre
@router.post("/", response_model=GenreResponse)
def create_genre(
        genre: GenreCreate,
        db: Session = Depends(get_db)):
    """
        Cria um novo gênro no banco de dados:

        - **genre_name**: recebe nome do gênero

    """
    db_genre = Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

#Retorna todos os genres
@router.get("/", response_model=list[GenreResponse])
def list_genre(
        db: Session = Depends(get_db)):
    """
        Retorna todos os gêneros cadastrados no banco de dados:

        - **genre_name**: retorna nome do gênero
        - **genre_id**: retorna id do gênereo

    """
    genres = db.query(Genre).all()
    return genres

#Lista todos os artists de um genre
@router.get("/{genre_id}/artists", response_model=list[ArtistResponse])
def get_genre_artists(
        genre_id: int,
        db: Session = Depends(get_db)):
    """
        Retorna todos os artistas de um gênero:

        - **genre_id**: recebe id do gênero

        Localiza gênero pelo id e retorna a lista de artistas do gênero e suas informações.
    """

    genre = db.get(Genre, genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre.artists

#Atualiza genre
@router.patch("/{genre_id}")
def update_genre(
    genre_id: int,
    updated_data: GenreUpdate,
    db: Session = Depends(get_db)):
    """
        Atualiza informações do gênero:

        - **genre_id**: recebe id do gênero

        Localiza gênero pelo id e permimte alteração dos dados

    """
    genre = db.get(Genre, genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre does not exist")

    update_genre = updated_data.model_dump(exclude_unset=True)

    for key, value in update_genre.items():
        setattr(genre, key, value)

    db.commit()
    db.refresh(genre)

    return genre

#Deleta genre
@router.delete("/{genre_id}")
def delete_genre(
        genre_id: int,
        db: Session = Depends(get_db)):
    """
        Deleta um gênero do banco de dados:

        - **genre_id**: recebe id do gênero

        Localiza gênero pelo id e remove o do banco de dados.

    """
    genre = db.get(Genre, genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre does not exist")

    genre.users.clear()
    genre.artists.clear()

    db.delete(genre)
    db.commit()

    return {"message": "Genre deleted successfully!"}