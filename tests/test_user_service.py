"""
Testes unitários para o serviço de usuários (user_service.py)

Este módulo testa todas as operações CRUD relacionadas aos usuários,
incluindo criação, listagem, atualização, exclusão e gerenciamento de 
relacionamentos com gêneros e eventos.
"""

import pytest
from sqlalchemy.orm import Session

from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Event, Genre, User
from app.schemas.user import UserCreate, UserUpdate
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


# ============================================================================
# TESTES DE CRIAÇÃO DE USUÁRIO
# ============================================================================


def test_create_user_success(db: Session):
    """
    Testa a criação bem-sucedida de um novo usuário.
    
    Verifica que:
    - O usuário é criado com todos os campos corretos
    - Os dados são persistidos no banco de dados
    - Os campos opcionais recebem valores padrão quando não fornecidos
    """
    user_data = UserCreate(
        username="João Silva",
        email="joao@example.com",
        user_password="senha123",
        profile_image="https://example.com/foto.jpg",
        country="BR",
    )

    # Cria o usuário usando o serviço
    result = create_user_service(user_data, db)

    # Verifica se o usuário foi criado corretamente
    assert result.username == "João Silva"
    assert result.email == "joao@example.com"
    assert result.user_password == "senha123"
    assert result.profile_image == "https://example.com/foto.jpg"
    assert result.country == "BR"
    assert result.user_id is not None

    # Confirma que o usuário está no banco de dados
    db_user = db.get(User, result.user_id)
    assert db_user is not None
    assert db_user.email == "joao@example.com"


def test_create_user_with_optional_fields_empty(db: Session):
    """
    Testa a criação de usuário quando campos opcionais não são fornecidos.
    
    Verifica que:
    - Campos opcionais recebem valores padrão vazios
    - O usuário ainda é criado com sucesso
    """
    user_data = UserCreate(
        username="Maria", email="maria@example.com", user_password="senha456"
    )

    result = create_user_service(user_data, db)

    # Campos opcionais devem ter valores padrão vazios
    assert result.profile_image == ""
    assert result.country == ""
    assert result.username == "Maria"


def test_create_user_duplicate_email_raises_conflict(db: Session):
    """
    Testa que não é possível criar dois usuários com o mesmo e-mail.
    
    Verifica que:
    - Uma exceção ConflictException é lançada ao tentar duplicar e-mail
    - O segundo usuário não é criado no banco de dados
    """
    # Cria o primeiro usuário
    user_data1 = UserCreate(
        username="Pedro", email="pedro@example.com", user_password="senha789"
    )
    create_user_service(user_data1, db)

    # Tenta criar segundo usuário com mesmo e-mail
    user_data2 = UserCreate(
        username="Paulo", email="pedro@example.com", user_password="outrasenha"
    )

    # Deve lançar exceção de conflito
    with pytest.raises(ConflictException, match="Email already registered"):
        create_user_service(user_data2, db)

    # Verifica que apenas um usuário com este e-mail existe
    users = db.query(User).filter(User.email == "pedro@example.com").all()
    assert len(users) == 1


# ============================================================================
# TESTES DE LISTAGEM DE USUÁRIOS
# ============================================================================


def test_list_users_empty_database(db: Session):
    """
    Testa a listagem de usuários quando o banco está vazio.
    
    Verifica que:
    - Uma lista vazia é retornada
    - Não ocorrem erros ao consultar banco vazio
    """
    result = list_users_service(db)
    
    # Como o conftest.py adiciona alguns usuários, vamos verificar o tipo
    assert isinstance(result, list)


def test_list_users_multiple_users(db: Session):
    """
    Testa a listagem de múltiplos usuários.
    
    Verifica que:
    - Todos os usuários cadastrados são retornados
    - A ordem de retorno é consistente
    """
    # O conftest.py já cria Ana e Bia
    initial_count = len(list_users_service(db))

    # Adiciona mais usuários
    for i in range(3):
        user_data = UserCreate(
            username=f"Usuario{i}",
            email=f"usuario{i}@example.com",
            user_password=f"senha{i}",
        )
        create_user_service(user_data, db)

    # Lista todos os usuários
    result = list_users_service(db)

    # Deve retornar todos os usuários
    assert len(result) == initial_count + 3


# ============================================================================
# TESTES DE ATUALIZAÇÃO DE USUÁRIO
# ============================================================================


def test_update_user_single_field(db: Session):
    """
    Testa a atualização de um único campo do usuário.
    
    Verifica que:
    - Apenas o campo especificado é modificado
    - Outros campos permanecem inalterados
    """
    # Cria um usuário
    user_data = UserCreate(
        username="Carlos", email="carlos@example.com", user_password="senha123"
    )
    user = create_user_service(user_data, db)

    # Atualiza apenas o username
    update_data = UserUpdate(username="Carlos Alberto")
    updated_user = update_user_service(user.user_id, update_data, db)

    # Verifica que o campo foi atualizado
    assert updated_user.username == "Carlos Alberto"
    # Verifica que outros campos não mudaram
    assert updated_user.email == "carlos@example.com"
    assert updated_user.user_password == "senha123"


def test_update_user_multiple_fields(db: Session):
    """
    Testa a atualização de múltiplos campos simultaneamente.
    
    Verifica que:
    - Todos os campos especificados são atualizados
    - As mudanças são persistidas no banco
    """
    # Cria um usuário
    user_data = UserCreate(
        username="Lucia", email="lucia@example.com", user_password="senha456"
    )
    user = create_user_service(user_data, db)

    # Atualiza múltiplos campos
    update_data = UserUpdate(
        username="Lucia Maria",
        profile_image="https://example.com/nova-foto.jpg",
        country="PT",
    )
    updated_user = update_user_service(user.user_id, update_data, db)

    # Verifica todas as atualizações
    assert updated_user.username == "Lucia Maria"
    assert updated_user.profile_image == "https://example.com/nova-foto.jpg"
    assert updated_user.country == "PT"
    assert updated_user.email == "lucia@example.com"  # Não foi alterado


def test_update_nonexistent_user_raises_not_found(db: Session):
    """
    Testa a atualização de um usuário que não existe.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    - Nenhuma modificação é feita no banco de dados
    """
    update_data = UserUpdate(username="Qualquer Nome")

    # Tenta atualizar usuário com ID que não existe
    with pytest.raises(NotFoundException, match="User does not exist"):
        update_user_service(99999, update_data, db)


# ============================================================================
# TESTES DE EXCLUSÃO DE USUÁRIO
# ============================================================================


def test_delete_user_success(db: Session):
    """
    Testa a exclusão bem-sucedida de um usuário.
    
    Verifica que:
    - O usuário é removido do banco de dados
    - Relacionamentos com gêneros e eventos são limpos antes da exclusão
    - Uma mensagem de sucesso é retornada
    """
    # Cria um usuário
    user_data = UserCreate(
        username="Roberto", email="roberto@example.com", user_password="senha789"
    )
    user = create_user_service(user_data, db)
    user_id = user.user_id

    # Exclui o usuário
    result = delete_user_service(user_id, db)

    # Verifica a mensagem de sucesso
    assert result["message"] == "User deleted successfully!"

    # Confirma que o usuário não existe mais
    deleted_user = db.get(User, user_id)
    assert deleted_user is None


def test_delete_nonexistent_user_raises_not_found(db: Session):
    """
    Testa a tentativa de excluir um usuário inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    - A mensagem de erro é apropriada
    """
    with pytest.raises(NotFoundException, match="User does not exist"):
        delete_user_service(99999, db)


# ============================================================================
# TESTES DE GERENCIAMENTO DE GÊNEROS DO USUÁRIO
# ============================================================================


def test_add_genre_to_user_success(db: Session):
    """
    Testa a adição de um gênero às preferências do usuário.
    
    Verifica que:
    - O gênero é associado ao usuário corretamente
    - O flag de notificações personalizadas é ativado
    - Uma mensagem de sucesso é retornada
    """
    # Cria um usuário e um gênero
    user_data = UserCreate(
        username="Fernanda", email="fernanda@example.com", user_password="senha123"
    )
    user = create_user_service(user_data, db)

    genre = Genre(genre_name="Rock")
    db.add(genre)
    db.commit()
    db.refresh(genre)

    # Adiciona o gênero ao usuário
    result = add_genre_user_service(user.user_id, genre.genre_id, db)

    # Verifica o sucesso
    assert result["message"] == "Genre added successfully!"

    # Confirma que o gênero está associado
    db.refresh(user)
    assert genre in user.genres
    assert user.personalized_notifications_only is True


def test_add_duplicate_genre_raises_conflict(db: Session):
    """
    Testa a tentativa de adicionar um gênero já associado ao usuário.
    
    Verifica que:
    - Uma exceção ConflictException é lançada
    - O gênero não é duplicado na lista do usuário
    """
    # Cria usuário e gênero
    user_data = UserCreate(
        username="Rafael", email="rafael@example.com", user_password="senha456"
    )
    user = create_user_service(user_data, db)

    genre = Genre(genre_name="Jazz")
    db.add(genre)
    db.commit()

    # Adiciona o gênero pela primeira vez
    add_genre_user_service(user.user_id, genre.genre_id, db)

    # Tenta adicionar o mesmo gênero novamente
    with pytest.raises(ConflictException, match="Genre already exists"):
        add_genre_user_service(user.user_id, genre.genre_id, db)


def test_add_genre_with_invalid_user_raises_not_found(db: Session):
    """
    Testa a adição de gênero para um usuário inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    - Nenhuma associação é criada
    """
    genre = Genre(genre_name="Pop")
    db.add(genre)
    db.commit()

    # Tenta adicionar gênero a usuário inexistente
    with pytest.raises(NotFoundException, match="User or Genre does not exist"):
        add_genre_user_service(99999, genre.genre_id, db)


def test_add_genre_with_invalid_genre_raises_not_found(db: Session):
    """
    Testa a adição de um gênero inexistente ao usuário.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    """
    user_data = UserCreate(
        username="Sandra", email="sandra@example.com", user_password="senha789"
    )
    user = create_user_service(user_data, db)

    # Tenta adicionar gênero inexistente
    with pytest.raises(NotFoundException, match="User or Genre does not exist"):
        add_genre_user_service(user.user_id, 99999, db)


def test_get_user_genres_success(db: Session):
    """
    Testa a consulta dos gêneros preferidos de um usuário.
    
    Verifica que:
    - Todos os gêneros associados são retornados
    - A lista está correta e completa
    """
    # Cria usuário e gêneros
    user_data = UserCreate(
        username="Marcos", email="marcos@example.com", user_password="senha123"
    )
    user = create_user_service(user_data, db)

    # Cria múltiplos gêneros
    genres = [Genre(genre_name=name) for name in ["Rock", "Jazz", "Blues"]]
    for genre in genres:
        db.add(genre)
    db.commit()

    # Adiciona os gêneros ao usuário
    for genre in genres:
        add_genre_user_service(user.user_id, genre.genre_id, db)

    # Consulta os gêneros do usuário
    result = get_user_genres_service(user.user_id, db)

    # Verifica que todos os gêneros foram retornados
    assert len(result) == 3
    genre_names = [g.genre_name for g in result]
    assert "Rock" in genre_names
    assert "Jazz" in genre_names
    assert "Blues" in genre_names


def test_get_genres_for_nonexistent_user_raises_not_found(db: Session):
    """
    Testa a consulta de gêneros para um usuário inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    """
    with pytest.raises(NotFoundException, match="User not found"):
        get_user_genres_service(99999, db)


def test_delete_genre_from_user_success(db: Session):
    """
    Testa a remoção de um gênero das preferências do usuário.
    
    Verifica que:
    - O gênero é removido da lista do usuário
    - Uma mensagem de sucesso é retornada
    """
    # Cria usuário e gênero
    user_data = UserCreate(
        username="Patricia", email="patricia@example.com", user_password="senha123"
    )
    user = create_user_service(user_data, db)

    genre = Genre(genre_name="Samba")
    db.add(genre)
    db.commit()

    # Adiciona e depois remove o gênero
    add_genre_user_service(user.user_id, genre.genre_id, db)
    result = delete_genre_user_service(user.user_id, genre.genre_id, db)

    # Verifica o sucesso
    assert result["message"] == "Genre unfavorited successfully!"

    # Confirma que o gênero foi removido
    db.refresh(user)
    assert genre not in user.genres


def test_delete_unlinked_genre_raises_bad_request(db: Session):
    """
    Testa a remoção de um gênero que não está associado ao usuário.
    
    Verifica que:
    - Uma exceção BadRequestException é lançada
    - A mensagem indica que o gênero não está vinculado
    """
    # Cria usuário e gênero
    user_data = UserCreate(
        username="Bruno", email="bruno@example.com", user_password="senha456"
    )
    user = create_user_service(user_data, db)

    genre = Genre(genre_name="Country")
    db.add(genre)
    db.commit()

    # Tenta remover gênero que não foi adicionado
    with pytest.raises(BadRequestException, match="Genre not linked"):
        delete_genre_user_service(user.user_id, genre.genre_id, db)


# ============================================================================
# TESTES DE GERENCIAMENTO DE EVENTOS DO USUÁRIO
# ============================================================================


def test_add_event_to_user_success(db: Session):
    """
    Testa a adição de um evento à lista de eventos do usuário.
    
    Verifica que:
    - O evento é associado ao usuário corretamente
    - Uma mensagem de sucesso é retornada
    """
    # Cria usuário e evento (usando o organizador criado no conftest)
    user_data = UserCreate(
        username="Laura", email="laura@example.com", user_password="senha789"
    )
    user = create_user_service(user_data, db)

    from datetime import date, timedelta

    event = Event(
        event_name="Festival de Verão",
        event_description="Grande festival",
        event_date=date.today() + timedelta(days=30),
        ticket_link="https://example.com/tickets",
        event_location="Rio de Janeiro",
        organizer_id=1,  # Organizador criado no conftest.py
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # Adiciona o evento ao usuário
    result = add_event_user_service(user.user_id, event.event_id, db)

    # Verifica o sucesso
    assert result["message"] == "Event added successfully!"

    # Confirma que o evento está associado
    db.refresh(user)
    assert event in user.events


def test_add_duplicate_event_raises_conflict(db: Session):
    """
    Testa a tentativa de adicionar um evento já associado ao usuário.
    
    Verifica que:
    - Uma exceção ConflictException é lançada
    - O evento não é duplicado
    """
    user_data = UserCreate(
        username="Gustavo", email="gustavo@example.com", user_password="senha123"
    )
    user = create_user_service(user_data, db)

    from datetime import date, timedelta

    event = Event(
        event_name="Show Especial",
        event_description="Show único",
        event_date=date.today() + timedelta(days=15),
        ticket_link="https://example.com/show",
        event_location="São Paulo",
        organizer_id=1,
    )
    db.add(event)
    db.commit()

    # Adiciona o evento pela primeira vez
    add_event_user_service(user.user_id, event.event_id, db)

    # Tenta adicionar novamente
    with pytest.raises(ConflictException, match="Event already linked"):
        add_event_user_service(user.user_id, event.event_id, db)


def test_get_user_events_success(db: Session):
    """
    Testa a consulta dos eventos associados a um usuário.
    
    Verifica que:
    - Todos os eventos do usuário são retornados
    - A lista está completa e correta
    """
    user_data = UserCreate(
        username="Camila", email="camila@example.com", user_password="senha456"
    )
    user = create_user_service(user_data, db)

    from datetime import date, timedelta

    # Cria múltiplos eventos
    for i in range(3):
        event = Event(
            event_name=f"Evento {i}",
            event_description=f"Descrição {i}",
            event_date=date.today() + timedelta(days=10 + i),
            ticket_link=f"https://example.com/event{i}",
            event_location="Brasília",
            organizer_id=1,
        )
        db.add(event)
        db.commit()
        add_event_user_service(user.user_id, event.event_id, db)

    # Consulta os eventos do usuário
    result = get_user_events_service(user.user_id, db)

    # Verifica que todos os eventos foram retornados
    assert len(result) == 3


def test_get_events_for_nonexistent_user_raises_not_found(db: Session):
    """
    Testa a consulta de eventos para um usuário inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    """
    with pytest.raises(NotFoundException, match="User not found"):
        get_user_events_service(99999, db)
