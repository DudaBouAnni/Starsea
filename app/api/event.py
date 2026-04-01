from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import SessionLocal
from app.models import Artist, event
from app.models.event import Event
from app.schemas.event import EventResponse, EventCreate, EventUpdate

router = APIRouter(prefix="/events", tags=["events"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Insere event
@router.post("/", response_model=EventResponse)
def create_event(
        event: EventCreate,
        db: Session = Depends(get_db)):
    """
        Cria um novo evento no banco de dados:

        - **event_name**: recebe nome do evento
        - **event_description**: recebe descrição do evento
        - **event_date**: recebe a data do evento
        - **ticket_link**: recebe link do site oficial de vendas de ingresso do evento
        - **event_location**: recebe a localização do evento
        - **organizer_id**: recebe o id do organizador do evento
        - **artists:** recebe lista de nomes de artistas que irão fazer parte do evento

    """

    #Verifica se a event_date não está no passado
    if event.event_date < date.today():
        raise HTTPException(400, "Event date cannot be in the past" )

    #Busca event pelo event_name
    exists = db.query(Event).filter_by(
        event_name = event.event_name
    ).first()

    #Verifica se event já existe no db
    if exists:
        raise HTTPException(400, "Event already exists")

    db_event = Event(
        event_name=event.event_name,
        event_description=event.event_description,
        event_date= event.event_date,
        ticket_link=event.ticket_link,
        event_location=event.event_location,
        organizer_id=event.organizer_id
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    #Procura artist na lista de algum event
    artist_objetcs = []

    for artist_name in event.artists:
        artist = db.query(Artist).filter(
            Artist.artist_name == artist_name
        ).first()


        if not artist:
            raise HTTPException(
                status_code= 400,
                detail=f"Artist '{artist_name}' does not exist"
            )

        artist_objetcs.append(artist)

    db_event.artists = artist_objetcs

    db.commit()

    return db_event

#Retorna todos os events
@router.get("/", response_model=List[EventResponse])
def list_events(
        db: Session = Depends(get_db)):
    """
            Retorna todos os eventos cadastrados no banco de dados:

            - **event_name**: retorna nome do evento
            - **event_description**: retorna descrição do evento
            - **event_date**: retorna a data do evento
            - **ticket_link**: retorna link do site oficial de vendas de ingresso do evento
            - **event_location**: retorna a localização do evento
            - **organizer_id**: retorna o id do organizador do evento
            - **artists:** retorna lista de nomes de artistas que irão fazer parte do evento

    """
    events = db.query(Event).all()
    return events

#Retorna todos os artists de um event
@router.get("/{event_id}/artists/{artist_id}")
def get_artist_event(
        event_id: int,
        db: Session = Depends(get_db)):
    """
        Retorna todos os artistas de um evento:

        - **event_id**: recebeid do evento

        Localiza evento pelo id e retorna a lista de artistas do evento e suas informações

    """

    event = db.get(Event, event_id)
    return event.artists

#Adiciona mais artists ao event
@router.post("/{event_id}/artists/{artist_id}")
def add_artist_event(
        event_id: int,
        artist_id: int,
        db: Session = Depends(get_db)):
    """
            Adiciona mais artistas ao evento:

            - **event_id**: recebe id do evento
            - **artist_id**: recebe id do artista

            recebe o id do evento e recebe o id do artista, então ele adiciona o artista ao evento

    """

    event = db.get(Event, event_id)
    artist = db.get(Artist, artist_id)

    #Excessão evento/artista existe no db
    if not event or not artist:
        raise HTTPException(400, "Event or artist does not exist")

    #Excessão artista repetido
    if artist in event.artists:
        raise HTTPException(400, "Artist already in event")

    event.artists.append(artist)

    db.commit()

    return {"message": "Artist added successfully!"}

#Atualiza event
@router.patch("/{event_id}")
def update_event(
    event_id: int,
    updated_data: EventUpdate,
    db: Session = Depends(get_db)):
    """
        Atualiza informações do evento:

        - **event_id**: recebe id do evento
        - **event_name**: retorna nome do evento
        - **event_description**: retorna descrição do evento
        - **event_date**: retorna a data do evento
        - **ticket_link**: retorna link do site oficial de vendas de ingresso do evento
        - **event_location**: retorna a localização do evento
        - **organizer_id**: retorna o id do organizador do evento
        - **artists:** retorna lista de nomes de artistas que irão fazer parte do evento

        Localiza evento pelo id e permimte alteração dos dados

    """

    event = db.get(Event, event_id)

    #Verifica se evento existe no db
    if not event:
        raise HTTPException(status_code=404, detail="Event does not exist")

    update_event = updated_data.model_dump(exclude_unset=True)

    for key, value in update_event.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    return event

#Deleta event
@router.delete("/{event_id}")
def delete_event(
        event_id: int,
        db: Session = Depends(get_db)):

    """
        Deleta evento:

        - **event_id**: recebe id do evento

        Localiza evento pelo id e remove o do db

    """

    event = db.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event does not exist")

    event.artists.clear()

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully!"}

#Deleta artist de um event
@router.delete("/{event_id}/artists/{artist_id}")
def remove_artist_event(
    event_id: int,
    artist_id: int,
    db: Session = Depends(get_db)
    ):

    """
        Atualiza informações do evento:

        - **event_id**: recebe id do evento
        - **artist_id**: recebe id do artista

        Localiza evento pelo id, recebe o id do artista desejado e remove o do db

    """

    event = db.get(Event, event_id)
    artist = db.get(Artist, artist_id)

    #Verifica se evento e/ou artista existe no db

    if not event or not artist:
        raise HTTPException(status_code=404, detail="Event or Artist does not exist")

    #

    if artist not in event.artists:
        raise HTTPException(status_code=400, detail="Artist not linked to this event")

    event.artists.remove(artist)

    db.commit()

    return {"message": "Artist removed from event"}