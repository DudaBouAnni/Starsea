from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
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

#Cria um novo artist
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

    #Define objeto genre
    genre_objects = []

    #Verifica se genere existe no db
    for genre_name in artist.genres:
        genre = db.query(Genre).filter_by(
            genre_name = genre_name
        ).first()

        if not genre:
            raise HTTPException(
                status_code=400,
                detail=f"Genre '{genre_name}' not found.")

        genre_objects.append(genre)

    db_artist.genres = genre_objects

    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)

    return db_artist

#Retorna todos os artists
@router.get("/", response_model=List[ArtistResponse])
def list_artists(
        db: Session = Depends(get_db)):
    """
        Retorna as seguintes informações de todos os artistas cadastrados no banco de dados:

       - **artist_name**: retorna nome do artista
       - **artist_id**: retorna id do artista
       - **genres**: retorna lista de gêneros do artista
    """
    return db.query(Artist).all()

#Adiciona genere a artist
@router.post("/{artist_id}/genres/{genre_id}", response_model=ArtistResponse)
def add_genre_to_artist(
    artist_id: int,
    genre_id: int,
    db: Session = Depends(get_db)):

    """
       Adiciona um novo gênero ao artista:

       - **artist_id**: recebe id do artista
       - **genre_id**: recebe id do genero

        Localiza artista pelo id e insere o gênero escolhido na lista de gêneros do artista.
    """

    artist = db.get(Artist, artist_id)
    genre = db.get(Genre, genre_id)

    #Verifica se artist ou genre existe no db
    if not artist or not genre:
        raise HTTPException(status_code=404, detail="Artist or Genre not found")

    artist.genres.append(genre)

    db.commit()

#Retorna todos events de um artist
@router.get("/{artist_id}/events", response_model=list[EventResponse])
def get_artist_events(
        artist_id: int,
        db: Session = Depends(get_db)):
    """
       Retorna todos os eventos de algum artista:

       - **artist_id**: recebe id do artista

    """

    artist = db.get(Artist, artist_id)

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    return artist.events

#Atualiza artist
@router.patch("/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: int,
    updated_data: ArtistUpdate,
    db: Session = Depends(get_db)
):
    """

       Atualiza informações do artista:

       - **artist_id**: recebe id do artista

       Localiza artista pelo id e permite alteração dos dados.

    """

    artist = db.get(Artist, artist_id)

    #Verifica se artist existe no db
    if not artist:
        raise HTTPException(status_code=404, detail="Artist does not exist")

    update_artist = updated_data.model_dump(exclude_unset=True)

    for key, value in update_artist.items():
        setattr(artist, key, value)

    db.commit()
    db.refresh(artist)

    return artist

#Deleta artist
@router.delete("/{artist_id}")
def delete_artist(
        artist_id: int,
        db: Session = Depends(get_db)):

    """
       Deleta artista do banco de dados.

       - **artist_id**: recebe id do artista

       Localiza artista pelo id e o remove do banco de dados.
    """

    artist = db.get(Artist, artist_id)

    #Verifica se artist existe no db
    if not artist:
        raise HTTPException(status_code=404, detail="Artist does not exist")

    artist.genres.clear()

    db.delete(artist)
    db.commit()

    return {"message": "Artist deleted successfully!"}

#Deleta genre de algum artist
@router.delete("/{artist_id}/genres/{genre_id}")
def remove_genre_artist(
    artist_id: int,
    genre_id: int,
    db: Session = Depends(get_db)
    ):
    """
       Remove algum genero de algum artista:

       - **artist_id**: recebe id do artista
       - **genre_id**: recebe id do gênero

       Localiza artista pelo id, depois localiza gênero do artista pelo id do gênero então o remove da lista de gêneros do artista.
    """

    artist = db.get(Artist, artist_id)
    genre = db.get(Genre, genre_id)

    #Verifica se artist ou genre existem no db
    if not artist or not genre:
        raise HTTPException(status_code=404, detail="Artist or Genre does not exist")

    #Verifica se genre está atrelado ao artist
    if genre not in artist.genres:
        raise HTTPException(status_code=400, detail="Genre not linked to this artist")

    artist.genres.remove(genre)

    db.commit()

    return {"message": "Genre removed from artist successfully!"}
