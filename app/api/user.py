from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import (
    add_event_user_service,
    add_genre_user_service,
    create_user_service,
    delete_genre_user_service,
    delete_user_service,
    get_user_events_service,
    get_user_genres_service,
    list_users_service,
    update_user_service,
)

router = APIRouter(prefix="/users", tags=["users"])


# Cria um usuário
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um usuário no banco de dados.

    - **username**: nome do usuário.
    - **email**: e-mail do usuário.
    - **username_password**: senha do usuário.
    """

    return create_user_service(user, db)


# Lista os usuários
@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """
    Retorna os usuários cadastrados no banco.

    - **user_id**: identificador do usuário.
    - **username**: nome do usuário.
    - **email**: e-mail do usuário.
    """

    return list_users_service(db)


# Adiciona um gênero ao usuário
@router.post("/{user_id}/genres/{genre_id}")
def add_genre_user(user_id: int, genre_id: int, db: Session = Depends(get_db)):
    """
    Adiciona um gênero à lista de gêneros do usuário.

    - **user_id**: identificador do usuário.
    - **genre_id**: identificador do gênero.

    Localiza os registros pelos identificadores e cria a associação.
    """

    return add_genre_user_service(user_id, genre_id, db)


# Retorna os gêneros do usuário
@router.get("/{user_id}/genres")
def get_user_genres(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna os gêneros do usuário.

    - **user_id**: identificador do usuário.

    Localiza o usuário pelo identificador e retorna sua lista de gêneros.
    """

    return get_user_genres_service(user_id, db)


# Adiciona um evento ao usuário
@router.post("/{user_id}/events/{event_id}")
def add_event_user(user_id: int, event_id: int, db: Session = Depends(get_db)):
    """
    Adiciona um evento à lista do usuário.

    - **user_id**: identificador do usuário.
    - **event_id**: identificador do evento.

    Localiza os registros e associa o evento ao usuário.
    """

    return add_event_user_service(user_id, event_id, db)


# Retorna os eventos do usuário
@router.get("/{user_id}/events")
def get_user_events(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna os eventos do usuário.

    - **user_id**: identificador do usuário.

    Localiza o usuário pelo identificador e retorna sua lista de eventos.
    """

    return get_user_events_service(user_id, db)


# Atualiza o usuário
@router.patch("/{user_id}")
def update_user(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados do usuário.

    - **user_id**: identificador do usuário.

    Localiza o usuário pelo identificador e permite atualizar seus dados.
    """

    return update_user_service(user_id, updated_data, db)


# Exclui o usuário
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Exclui o usuário do banco de dados.

    - **user_id**: identificador do usuário.

    Localiza o usuário pelo identificador e remove seu registro.
    """

    return delete_user_service(user_id, db)


# Remove um gênero do usuário
@router.delete("/{user_id}/genres/{genere_id}")
def delete_genre_user(user_id: int, genere_id: int, db: Session = Depends(get_db)):
    """
    Remove um gênero do usuário.

    - **user_id**: identificador do usuário.
    - **genre_id**: identificador do gênero.

    Localiza os registros e remove o gênero da lista de preferências do usuário.
    """

    return delete_genre_user_service(user_id, genere_id, db)
