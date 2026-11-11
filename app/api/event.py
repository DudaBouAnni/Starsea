from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services.event_service import (
    add_artist_event_service,
    create_event_service,
    delete_event_service,
    get_event_artists_service,
    list_events_service,
    remove_artist_event_service,
    update_event_service,
)
from app.services.maps_service import get_event_map_url

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/{event_id}/map", response_class=RedirectResponse)
def open_event_map(event_id: int, db: Session = Depends(get_db)):
    """Abre o Maps no local do show. A pessoa pode tocar em Rotas no próprio Maps."""
    return RedirectResponse(get_event_map_url(event_id, db), status_code=307)


# Cria um evento
@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Cria um evento no banco de dados.

    - **event_name**: nome do evento.
    - **event_description**: descrição do evento.
    - **event_date**: data do evento.
    - **ticket_link**: link oficial de venda de ingressos.
    - **event_location**: local do evento.
    - **organizer_id**: identificador do organizador.
    - **artists**: lista de artistas participantes.
    """
    return create_event_service(event, db)


# Lista os eventos
@router.get("/", response_model=List[EventResponse])
def list_events(db: Session = Depends(get_db)):
    """
    Retorna os dados dos eventos cadastrados no banco.

    - **event_name**: nome do evento.
    - **event_description**: descrição do evento.
    - **event_date**: data do evento.
    - **ticket_link**: link oficial de venda de ingressos.
    - **event_location**: local do evento.
    - **organizer_id**: identificador do organizador.
    - **artists**: lista de artistas participantes.
    """
    return list_events_service(db)


# Consulta os artistas do evento
@router.get("/{event_id}/artists/{artist_id}")
def get_artist_event(event_id: int, artist_id: int, db: Session = Depends(get_db)):
    """
    Retorna os artistas participantes do evento.

    - **event_id**: identificador do evento.

    Localiza o evento pelo identificador e retorna os dados dos artistas associados.
    """
    return get_event_artists_service(event_id, artist_id, db)


# Adiciona um artista ao evento
@router.post("/{event_id}/artists/{artist_id}")
def add_artist_event(event_id: int, artist_id: int, db: Session = Depends(get_db)):
    """
    Adiciona um artista ao evento.

    - **event_id**: identificador do evento.
    - **artist_id**: identificador do artista.

    Localiza os registros e associa o artista ao evento.
    """

    return add_artist_event_service(event_id, artist_id, db)


# Atualiza o evento
@router.patch("/{event_id}")
def update_event(event_id: int, updated_data: EventUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados do evento.

    - **event_id**: identificador do evento.
    - **event_name**: nome do evento.
    - **event_description**: descrição do evento.
    - **event_date**: data do evento.
    - **ticket_link**: link oficial de venda de ingressos.
    - **event_location**: local do evento.
    - **organizer_id**: identificador do organizador.
    - **artists**: lista de artistas participantes.

    Localiza o evento pelo identificador e permite atualizar seus dados.
    """
    return update_event_service(event_id, updated_data, db)


# Exclui o evento
@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    Exclui o evento do banco de dados.

    - **event_id**: identificador do evento.

    Localiza o evento pelo identificador e remove seu registro.
    """
    return delete_event_service(event_id, db)


# Remove um artista do evento
@router.delete("/{event_id}/artists/{artist_id}")
def remove_artist_event(event_id: int, artist_id: int, db: Session = Depends(get_db)):
    """
    Remove um artista da lista de participantes do evento.

    - **event_id**: identificador do evento.
    - **artist_id**: identificador do artista.

    Localiza os registros e desfaz a associação entre o evento e o artista.
    """
    return remove_artist_event_service(event_id, artist_id, db)
