from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models.genre import Genre
from app.schemas.artist import ArtistResponse
from app.schemas.genre import GenreCreate, GenreResponse, GenreUpdate
from app.services.genre_service import (
    create_genre_service,
    delete_genre_service,
    get_genre_artists_service,
    list_genre_service,
    update_genre_service,
)

router = APIRouter(prefix="/genres", tags=["genres"])


# Cria um gênero
@router.post("/", response_model=GenreResponse)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    """
    Cria um gênero no banco de dados.

    - **genre_name**: nome do gênero.
    """

    return create_genre_service(genre, db)


# Lista os gêneros
@router.get("/", response_model=list[GenreResponse])
def list_genre(db: Session = Depends(get_db)):
    """
    Retorna as informações dos gêneros cadastrados no banco.

    - **genre_name**: nome do gênero.
    - **genre_id**: identificador do gênero.
    """
    return list_genre_service(db)


# Lista os artistas de um gênero
@router.get("/{genre_id}/artists", response_model=list[ArtistResponse])
def get_genre_artists(genre_id: int, db: Session = Depends(get_db)):
    """
    Retorna os artistas associados ao gênero.

    - **genre_id**: identificador do gênero.

    Localiza o gênero pelo identificador e retorna a lista de artistas e seus dados.
    """

    return get_genre_artists_service(genre_id, db)


# Atualiza o gênero
@router.patch("/{genre_id}")
def update_genre(genre_id: int, updated_data: GenreUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados do gênero.

    - **genre_id**: identificador do gênero.

    Localiza o gênero pelo identificador e permite atualizar seus dados.
    """

    return update_genre_service(genre_id, updated_data, db)


# Exclui o gênero
@router.delete("/{genre_id}")
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    Exclui o gênero do banco de dados.

    - **genre_id**: identificador do gênero.

    Localiza o gênero pelo identificador e remove seu registro.
    """

    return delete_genre_service(genre_id, db)
