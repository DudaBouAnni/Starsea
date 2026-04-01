from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models import Event
from app.models.genre import Genre
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Insere user
@router.post("/", response_model=UserResponse)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db)):
    """
       Cria um usuário no banco de dados:

        - **username**: recebe nome do usuário
        - **email**: recebe email do usuário
        - **username_password**: recebe senha do usuário

    """

    db_user = User(
    username = user.username,
    user_password = user.user_password,
    email = user.email,
    )

    db.add(db_user),
    db.commit(),
    db.refresh(db_user)

    return db_user

#Lista todos os users
@router.get("/", response_model=list[UserResponse])
def list_users(
        db: Session = Depends(get_db)):
    """
        Retorna todos os usuários cadastrados no banco de dados:

        - **user_id**: retorna id do usuário
        - **username**: retorna nome do usuário
        - **email**: retorna email do usuário

    """

    users = db.query(User).all()
    return users

#Adicionar genre ao user
@router.post("/{user_id}/genres/{genre_id}")
def add_genre_user(
        user_id: int,
        genre_id: int,
        db: Session = Depends(get_db)):
    """
        Adiciona um novo gênero ao usuário:

        - **user_id**: recebe id do usuário
        - **genre_id**: recebe id do gênero

        Localiza usuário pelo id e insere o gênero escolhido na lista de gêneros do usuário.

    """

    user = db.get(User, user_id)
    genre = db.get(Genre, genre_id)

    #Verifica se user e/ou genre existe no db
    if not user or not genre:
        raise HTTPException(status_code=404, detail="User or Genre does not exist")

    #Verifica se user já tem esse genre associado
    if genre in user.genres:
        return {"message": "Genre already added"}

    user.genres.append(genre)

    db.commit()

    return {"message": "Genre added successfully!"}

#Retorna todos os genres de um user
@router.get("/{user_id}/genres")
def get_user_genres(
        user_id: int,
        db: Session = Depends(get_db)):
    """
        Retorna todos os gêneros de algum usuário:

        - **user_id**: recebe id do usuário

        Localiza usuário pelo id e retorna a lista de gêneros do usuário.

    """

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.genres

#Adicionar events ao user
@router.post("/{user_id}/events/{event_id}")
def add_event_user(
        user_id: int,
        event_id: int,
        db: Session = Depends(get_db)):
    """
        Adiciona um novo evento ao usuário:

        - **user_id**: recebe id do usuário
        - **event_id**: recebe id do evento

        Localiza usuário pelo id e insere o evento escolhido na lista de eventos do usuário.

    """
    user = db.get(User, user_id)
    event = db.get(Event, event_id)

    #Verifica se user e/ou event existe no db
    if not user or not event:
        raise HTTPException(status_code=404, detail="User or Event does not exist")

    #Verifica se user já tem esse event associado
    if event in user.events:
        return {"message": "Event already added"}

    user.events.append(event)

    db.commit()

    return {"message": "Genre added successfully!"}

#Retorna todos os events de um user
@router.get("/{user_id}/events")
def get_user_events(
        user_id: int,
        db: Session = Depends(get_db)):

    """
        Retorna todos os eventos de algum usuário:

        - **user_id**: recebe id do usuário

        Localiza usuário pelo id e retorna a lista de eventos do usuário.

    """

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.events

#Atualiza user
@router.patch("/{user_id}")
def update_user(
    user_id: int,
    updated_data: UserUpdate,
    db: Session = Depends(get_db)):

    """
        Atualiza usuário:

        - **user_id**: recebe id do usuário

        Localiza usuário pelo id e permite a alteração dos dados.

    """

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    update_user = updated_data.model_dump(exclude_unset=True)

    for key, value in update_user.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

#Deleta user
@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)):

    """
        Deleta usuário do banco de dados:

        - **user_id**: recebe id do usuário

        Localiza usuário pelo id e remove o do banco de dados.

    """

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    user.genres.clear()
    user.events.clear()

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully!"}

#Deleta algum genre do user
@router.delete("/{user_id}/genres/{genere_id}")
def delete_genre_user(
        user_id: int,
        genere_id: int,
        db: Session = Depends(get_db)):

    """
        Deleta um gênero de um usuário:

        - **user_id**: recebe id do usuário
        - **genre_id**: recebe id do gênero

        Localiza usuário pelo id, localiza gênero pelo id e o remove da lista de gêneros do usuário.

    """

    user = db.get(User, user_id)
    genre = db.get(Genre, genere_id)

    #Verifica se user e/ou genre existem no db
    if not user or not genre:
        raise HTTPException(status_code=404, detail="User or Genre does not exist")

    #Verifica de genre está na lista de genres do usuário
    if genre not in user.genres:
        raise HTTPException(status_code=404, detail="Genre not linked")

    user.genres.remove(genre)

    db.commit()

    return {"message": "Genre unfavorited successfully!"}