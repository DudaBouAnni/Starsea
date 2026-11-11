from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.artist import ArtistCreate, ArtistResponse, ArtistUpdate
from app.schemas.event import EventResponse
from app.services.artist_service import (
    add_genre_artist_service,
    create_artist_service,
    delete_artist_service,
    get_artist_events_service,
    list_artists_service,
    remove_artist_genres_service,
    update_artist_service,
)

router = APIRouter(prefix="/artists", tags=["artists"])


# Cria um artista
@router.post("/", response_model=ArtistResponse)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    """
    Cria um novo artista no banco de dados:

    - **artist_name**: recebe nome do artista
    - **genres**: recebe nomes de gêneros existentes em lista
    """

    return create_artist_service(artist, db)


# Retorna todos os artistas
@router.get("/", response_model=List[ArtistResponse])
def list_artists(db: Session = Depends(get_db)):
    """
    Retorna as informações dos artistas cadastrados no banco.

    - **artist_name**: nome do artista.
    - **artist_id**: identificador do artista.
    - **genres**: lista de gêneros do artista.
    """
    return list_artists_service(db)


# Adiciona um gênero ao artista
@router.post("/{artist_id}/genres/{genre_id}", response_model=ArtistResponse)
def add_genre_artist(artist_id: int, genre_id: int, db: Session = Depends(get_db)):
    """
    Adiciona um gênero à lista de gêneros do artista.

    - **artist_id**: identificador do artista.
    - **genre_id**: identificador do gênero.

    Localiza os registros pelos identificadores e cria a associação.
    """
    return add_genre_artist_service(artist_id, genre_id, db)


# Retorna os eventos do artista
@router.get("/{artist_id}/events", response_model=list[EventResponse])
def get_artist_events(artist_id: int, db: Session = Depends(get_db)):
    """
    Retorna todos os eventos do artista.

    - **artist_id**: identificador do artista.
    """

    return get_artist_events_service(artist_id, db)


# Atualiza o artista
@router.patch("/{artist_id}", response_model=ArtistResponse)
def update_artist(artist_id: int, updated_data: ArtistUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados do artista.

    - **artist_id**: identificador do artista.

    Localiza o artista pelo identificador e permite atualizar seus dados.
    """

    return update_artist_service(artist_id, updated_data, db)


# Exclui o artista
@router.delete("/{artist_id}")
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    """
    Exclui o artista do banco de dados.

    - **artist_id**: identificador do artista.

    Localiza o artista pelo identificador e remove seu registro.
    """

    return delete_artist_service(artist_id, db)


# Remove um gênero do artista
@router.delete("/{artist_id}/genres/{genre_id}")
def remove_genre_artist(artist_id: int, genre_id: int, db: Session = Depends(get_db)):
    """
    Remove um gênero da lista de gêneros do artista.

    - **artist_id**: identificador do artista.
    - **genre_id**: identificador do gênero.

    Localiza o artista e o gênero e desfaz a associação.
    """

    return remove_artist_genres_service(artist_id, genre_id, db)
