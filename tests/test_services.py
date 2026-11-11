"""
Testes das funções dos serviços
"""

import pytest
from datetime import date, timedelta

from app.models import Artist, Event, Genre, Organizer, User
from app.schemas.genre import GenreCreate, GenreUpdate
from app.schemas.artist import ArtistCreate, ArtistUpdate
from app.schemas.event import EventCreate, EventUpdate
from app.schemas.organizer import OrganizerCreate, OrganizerUpdate
from app.schemas.user import UserCreate, UserUpdate

from app.services.genre_service import (
    create_genre_service,
    list_genre_service,
    get_genre_artists_service,
    update_genre_service,
    delete_genre_service,
)

from app.services.artist_service import (
    create_artist_service,
    list_artists_service,
    add_genre_artist_service,
    get_artist_events_service,
    update_artist_service,
    delete_artist_service,
    remove_artist_genres_service,
)

from app.services.event_service import (
    create_event_service,
    list_events_service,
    get_event_artists_service,
    add_artist_event_service,
    update_event_service,
    delete_event_service,
    remove_artist_event_service,
)

from app.services.organizer_service import (
    create_organizer_service,
    list_organizers_service,
    get_organizer_events_service,
    update_organizer_service,
    delete_organizer_service,
)

from app.services.user_service import (
    create_user_service,
    list_users_service,
    add_genre_user_service,
    get_user_genres_service,
    add_event_user_service,
    get_user_events_service,
    update_user_service,
    delete_user_service,
    delete_genre_user_service,
)

from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.exceptions.BadRequestException import BadRequestException


# ===========================================================================
# GENRE SERVICE
# ===========================================================================


def test_create_genre_service(db):
    """Testa criar gênero"""
    data = GenreCreate(genre_name="Rock")
    result = create_genre_service(data, db)
    
    assert result.genre_name == "Rock"
    assert result.genre_id is not None


def test_create_genre_service_duplicado(db):
    """Testa criar gênero duplicado - deve dar erro"""
    data = GenreCreate(genre_name="Pop")
    create_genre_service(data, db)
    
    with pytest.raises(ConflictException):
        create_genre_service(data, db)


def test_list_genre_service(db):
    """Testa listar gêneros"""
    create_genre_service(GenreCreate(genre_name="Jazz"), db)
    create_genre_service(GenreCreate(genre_name="Blues"), db)
    
    result = list_genre_service(db)
    assert len(result) >= 2


def test_get_genre_artists_service(db):
    """Testa buscar artistas de um gênero"""
    genre = Genre(genre_name="Metal")
    db.add(genre)
    db.commit()
    
    result = get_genre_artists_service(genre.genre_id, db)
    assert result == []


def test_get_genre_artists_service_not_found(db):
    """Testa buscar artistas de gênero inexistente"""
    with pytest.raises(NotFoundException):
        get_genre_artists_service(99999, db)


def test_update_genre_service(db):
    """Testa atualizar gênero"""
    data = GenreCreate(genre_name="Rap")
    genre = create_genre_service(data, db)
    
    update = GenreUpdate(genre_name="Hip Hop")
    result = update_genre_service(genre.genre_id, update, db)
    
    assert result.genre_name == "Hip Hop"


def test_update_genre_service_not_found(db):
    """Testa atualizar gênero inexistente"""
    update = GenreUpdate(genre_name="Teste")
    
    with pytest.raises(NotFoundException):
        update_genre_service(99999, update, db)


def test_delete_genre_service(db):
    """Testa deletar gênero"""
    data = GenreCreate(genre_name="Temporário")
    genre = create_genre_service(data, db)
    
    result = delete_genre_service(genre.genre_id, db)
    assert result["message"] == "Genre deleted successfully!"


def test_delete_genre_service_not_found(db):
    """Testa deletar gênero inexistente"""
    with pytest.raises(NotFoundException):
        delete_genre_service(99999, db)


# ===========================================================================
# ARTIST SERVICE
# ===========================================================================


def test_create_artist_service(db):
    """Testa criar artista"""
    data = ArtistCreate(artist_name="Beatles", spotify_id=None, genres=[])
    result = create_artist_service(data, db)
    
    assert result.artist_name == "Beatles"
    assert result.artist_id is not None


def test_create_artist_service_with_spotify(db):
    """Testa criar artista com spotify_id"""
    data = ArtistCreate(artist_name="Queen", spotify_id="spot123", genres=[])
    result = create_artist_service(data, db)
    
    assert result.spotify_id == "spot123"


def test_create_artist_service_spotify_duplicado(db):
    """Testa criar artista com spotify_id duplicado"""
    data1 = ArtistCreate(artist_name="A1", spotify_id="same123", genres=[])
    create_artist_service(data1, db)
    
    data2 = ArtistCreate(artist_name="A2", spotify_id="same123", genres=[])
    with pytest.raises(ConflictException):
        create_artist_service(data2, db)


def test_create_artist_service_with_genres(db):
    """Testa criar artista com gêneros"""
    db.add(Genre(genre_name="Rock"))
    db.commit()
    
    data = ArtistCreate(artist_name="AC/DC", spotify_id=None, genres=["Rock"])
    result = create_artist_service(data, db)
    
    assert len(result.genres) == 1


def test_create_artist_service_genre_not_found(db):
    """Testa criar artista com gênero inexistente"""
    data = ArtistCreate(artist_name="Test", spotify_id=None, genres=["Inexistente"])
    
    with pytest.raises(NotFoundException):
        create_artist_service(data, db)


def test_list_artists_service(db):
    """Testa listar artistas"""
    create_artist_service(ArtistCreate(artist_name="A1", genres=[]), db)
    create_artist_service(ArtistCreate(artist_name="A2", genres=[]), db)
    
    result = list_artists_service(db)
    assert len(result) >= 2


def test_add_genre_artist_service(db):
    """Testa adicionar gênero ao artista"""
    artist = Artist(artist_name="Banda")
    genre = Genre(genre_name="Rock")
    db.add_all([artist, genre])
    db.commit()
    
    result = add_genre_artist_service(artist.artist_id, genre.genre_id, db)
    assert genre in result.genres


def test_add_genre_artist_service_not_found(db):
    """Testa adicionar gênero a artista inexistente"""
    with pytest.raises(NotFoundException):
        add_genre_artist_service(99999, 99999, db)


def test_add_genre_artist_service_duplicado(db):
    """Testa adicionar gênero já existente"""
    artist = Artist(artist_name="Banda")
    genre = Genre(genre_name="Rock")
    db.add_all([artist, genre])
    db.commit()
    
    add_genre_artist_service(artist.artist_id, genre.genre_id, db)
    
    with pytest.raises(ConflictException):
        add_genre_artist_service(artist.artist_id, genre.genre_id, db)


def test_get_artist_events_service(db):
    """Testa buscar eventos do artista"""
    artist = Artist(artist_name="Banda")
    db.add(artist)
    db.commit()
    
    result = get_artist_events_service(artist.artist_id, db)
    assert result == []


def test_get_artist_events_service_not_found(db):
    """Testa buscar eventos de artista inexistente"""
    with pytest.raises(NotFoundException):
        get_artist_events_service(99999, db)


def test_update_artist_service(db):
    """Testa atualizar artista"""
    data = ArtistCreate(artist_name="Nome Antigo", genres=[])
    artist = create_artist_service(data, db)
    
    update = ArtistUpdate(artist_name="Nome Novo")
    result = update_artist_service(artist.artist_id, update, db)
    
    assert result.artist_name == "Nome Novo"


def test_update_artist_service_not_found(db):
    """Testa atualizar artista inexistente"""
    update = ArtistUpdate(artist_name="Test")
    
    with pytest.raises(NotFoundException):
        update_artist_service(99999, update, db)


def test_update_artist_service_spotify_duplicado(db):
    """Testa atualizar com spotify_id duplicado"""
    a1 = create_artist_service(ArtistCreate(artist_name="A1", spotify_id="id1", genres=[]), db)
    a2 = create_artist_service(ArtistCreate(artist_name="A2", spotify_id="id2", genres=[]), db)
    
    update = ArtistUpdate(spotify_id="id1")
    with pytest.raises(ConflictException):
        update_artist_service(a2.artist_id, update, db)


def test_delete_artist_service(db):
    """Testa deletar artista"""
    data = ArtistCreate(artist_name="Temp", genres=[])
    artist = create_artist_service(data, db)
    
    result = delete_artist_service(artist.artist_id, db)
    assert result["message"] == "Arists deleted successfully!"


def test_delete_artist_service_not_found(db):
    """Testa deletar artista inexistente"""
    with pytest.raises(NotFoundException):
        delete_artist_service(99999, db)


def test_remove_artist_genres_service(db):
    """Testa remover gênero do artista"""
    artist = Artist(artist_name="Banda")
    genre = Genre(genre_name="Rock")
    db.add_all([artist, genre])
    db.commit()
    
    artist.genres.append(genre)
    db.commit()
    
    result = remove_artist_genres_service(artist.artist_id, genre.genre_id, db)
    assert result["message"] == "Artist removed from Genre successfully!"


def test_remove_artist_genres_service_not_found(db):
    """Testa remover gênero de artista inexistente"""
    with pytest.raises(NotFoundException):
        remove_artist_genres_service(99999, 99999, db)


# ===========================================================================
# EVENT SERVICE
# ===========================================================================


def test_create_event_service(db):
    """Testa criar evento"""
    data = EventCreate(
        event_name="Festival",
        event_description="Show",
        event_date=date.today() + timedelta(days=30),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1,
        artists=[]
    )
    result = create_event_service(data, db)
    
    assert result.event_name == "Festival"
    assert result.event_id is not None


def test_create_event_service_data_passado(db):
    """Testa criar evento com data no passado"""
    data = EventCreate(
        event_name="Teste",
        event_description="Show",
        event_date=date.today() - timedelta(days=1),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1,
        artists=[]
    )
    
    with pytest.raises(BadRequestException):
        create_event_service(data, db)


def test_create_event_service_duplicado(db):
    """Testa criar evento duplicado"""
    data = EventCreate(
        event_name="Único",
        event_description="Show",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1,
        artists=[]
    )
    create_event_service(data, db)
    
    with pytest.raises(ConflictException):
        create_event_service(data, db)


def test_create_event_service_organizer_not_found(db):
    """Testa criar evento com organizador inexistente"""
    data = EventCreate(
        event_name="Test",
        event_description="Show",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=99999,
        artists=[]
    )
    
    with pytest.raises(NotFoundException):
        create_event_service(data, db)


def test_create_event_service_with_artists(db):
    """Testa criar evento com artistas"""
    db.add(Artist(artist_name="Banda1"))
    db.commit()
    
    data = EventCreate(
        event_name="Show",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1,
        artists=["Banda1"]
    )
    result = create_event_service(data, db)
    
    assert len(result.artists) == 1


def test_create_event_service_artist_not_found(db):
    """Testa criar evento com artista inexistente"""
    data = EventCreate(
        event_name="Show",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1,
        artists=["Inexistente"]
    )
    
    with pytest.raises(NotFoundException):
        create_event_service(data, db)


def test_list_events_service(db):
    """Testa listar eventos"""
    result = list_events_service(db)
    assert isinstance(result, list)


def test_get_event_artists_service(db):
    """Testa buscar artistas do evento"""
    event = Event(
        event_name="Show",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1
    )
    db.add(event)
    db.commit()
    
    result = get_event_artists_service(event.event_id, db)
    assert result == []


def test_get_event_artists_service_not_found(db):
    """Testa buscar artistas de evento inexistente"""
    with pytest.raises(NotFoundException):
        get_event_artists_service(99999, db)


def test_add_artist_event_service(db):
    """Testa adicionar artista ao evento"""
    event = Event(
        event_name="Show",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1
    )
    artist = Artist(artist_name="Banda")
    db.add_all([event, artist])
    db.commit()
    
    result = add_artist_event_service(event.event_id, artist.artist_id, db)
    assert result["message"] == "Artist added successfully!"


def test_add_artist_event_service_not_found(db):
    """Testa adicionar artista a evento inexistente"""
    with pytest.raises(NotFoundException):
        add_artist_event_service(99999, 99999, db)


def test_add_artist_event_service_duplicado(db):
    """Testa adicionar artista já existente ao evento"""
    event = Event(
        event_name="Show",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1
    )
    artist = Artist(artist_name="Banda")
    db.add_all([event, artist])
    db.commit()
    
    add_artist_event_service(event.event_id, artist.artist_id, db)
    
    with pytest.raises(ConflictException):
        add_artist_event_service(event.event_id, artist.artist_id, db)


def test_update_event_service(db):
    """Testa atualizar evento"""
    event = Event(
        event_name="Antigo",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1
    )
    db.add(event)
    db.commit()
    
    update = EventUpdate(event_name="Novo")
    result = update_event_service(event.event_id, update, db)
    
    assert result.event_name == "Novo"


def test_update_event_service_not_found(db):
    """Testa atualizar evento inexistente"""
    update = EventUpdate(event_name="Test")
    
    with pytest.raises(NotFoundException):
        update_event_service(99999, update, db)


def test_delete_event_service(db):
    """Testa deletar evento"""
    event = Event(
        event_name="Temp",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1
    )
    db.add(event)
    db.commit()
    
    delete_event_service(event.event_id, db)
    assert db.get(Event, event.event_id) is None


def test_delete_event_service_not_found(db):
    """Testa deletar evento inexistente"""
    with pytest.raises(NotFoundException):
        delete_event_service(99999, db)


def test_remove_artist_event_service(db):
    """Testa remover artista do evento"""
    event = Event(
        event_name="Show",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1
    )
    artist = Artist(artist_name="Banda")
    db.add_all([event, artist])
    db.commit()
    
    event.artists.append(artist)
    db.commit()
    
    result = remove_artist_event_service(event.event_id, artist.artist_id, db)
    assert result["message"] == "Artist removed successfully!"


def test_remove_artist_event_service_not_found(db):
    """Testa remover artista de evento inexistente"""
    with pytest.raises(NotFoundException):
        remove_artist_event_service(99999, 99999, db)


# ===========================================================================
# ORGANIZER SERVICE
# ===========================================================================


def test_create_organizer_service(db):
    """Testa criar organizador"""
    data = OrganizerCreate(organizer_name="Produtora XYZ")
    result = create_organizer_service(data, db)
    
    assert result.organizer_name == "Produtora XYZ"
    assert result.organizer_id is not None


def test_create_organizer_service_duplicado(db):
    """Testa criar organizador duplicado"""
    data = OrganizerCreate(organizer_name="Único")
    create_organizer_service(data, db)
    
    with pytest.raises(ConflictException):
        create_organizer_service(data, db)


def test_list_organizers_service(db):
    """Testa listar organizadores"""
    result = list_organizers_service(db)
    assert isinstance(result, list)


def test_update_organizer_service(db):
    """Testa atualizar organizador"""
    data = OrganizerCreate(organizer_name="Antigo")
    org = create_organizer_service(data, db)
    
    update = OrganizerUpdate(organizer_name="Novo")
    result = update_organizer_service(org.organizer_id, update, db)
    
    assert result.organizer_name == "Novo"


def test_update_organizer_service_not_found(db):
    """Testa atualizar organizador inexistente"""
    update = OrganizerUpdate(organizer_name="Test")
    
    with pytest.raises(NotFoundException):
        update_organizer_service(99999, update, db)


def test_delete_organizer_service(db):
    """Testa deletar organizador"""
    data = OrganizerCreate(organizer_name="Temp")
    org = create_organizer_service(data, db)
    
    result = delete_organizer_service(org.organizer_id, db)
    assert result["message"] == "Organizer deleted successfully!"


def test_delete_organizer_service_not_found(db):
    """Testa deletar organizador inexistente"""
    with pytest.raises(NotFoundException):
        delete_organizer_service(99999, db)


# ===========================================================================
# USER SERVICE
# ===========================================================================


def test_create_user_service(db):
    """Testa criar usuário"""
    data = UserCreate(
        username="João",
        email="joao@test.com",
        user_password="senha123"
    )
    result = create_user_service(data, db)
    
    assert result.username == "João"
    assert result.user_id is not None


def test_create_user_service_email_duplicado(db):
    """Testa criar usuário com email duplicado"""
    data = UserCreate(
        username="User1",
        email="unico@test.com",
        user_password="senha"
    )
    create_user_service(data, db)
    
    data2 = UserCreate(
        username="User2",
        email="unico@test.com",
        user_password="senha"
    )
    
    with pytest.raises(ConflictException):
        create_user_service(data2, db)


def test_list_users_service(db):
    """Testa listar usuários"""
    result = list_users_service(db)
    assert isinstance(result, list)


def test_add_genre_user_service(db):
    """Testa adicionar gênero ao usuário"""
    user = User(username="Test", email="test@test.com", user_password="senha")
    genre = Genre(genre_name="Rock")
    db.add_all([user, genre])
    db.commit()
    
    result = add_genre_user_service(user.user_id, genre.genre_id, db)
    assert result["message"] == "Genre added successfully!"


def test_add_genre_user_service_not_found(db):
    """Testa adicionar gênero a usuário inexistente"""
    with pytest.raises(NotFoundException):
        add_genre_user_service(99999, 99999, db)


def test_add_genre_user_service_duplicado(db):
    """Testa adicionar gênero já existente"""
    user = User(username="Test", email="test@test.com", user_password="senha")
    genre = Genre(genre_name="Rock")
    db.add_all([user, genre])
    db.commit()
    
    add_genre_user_service(user.user_id, genre.genre_id, db)
    
    with pytest.raises(ConflictException):
        add_genre_user_service(user.user_id, genre.genre_id, db)


def test_get_user_genres_service(db):
    """Testa buscar gêneros do usuário"""
    user = User(username="Test", email="test@test.com", user_password="senha")
    db.add(user)
    db.commit()
    
    result = get_user_genres_service(user.user_id, db)
    assert result == []


def test_get_user_genres_service_not_found(db):
    """Testa buscar gêneros de usuário inexistente"""
    with pytest.raises(NotFoundException):
        get_user_genres_service(99999, db)


def test_add_event_user_service(db):
    """Testa adicionar evento ao usuário"""
    user = User(username="Test", email="test@test.com", user_password="senha")
    event = Event(
        event_name="Show",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1
    )
    db.add_all([user, event])
    db.commit()
    
    result = add_event_user_service(user.user_id, event.event_id, db)
    assert result["message"] == "Event added successfully!"


def test_add_event_user_service_not_found(db):
    """Testa adicionar evento a usuário inexistente"""
    with pytest.raises(NotFoundException):
        add_event_user_service(99999, 99999, db)


def test_add_event_user_service_duplicado(db):
    """Testa adicionar evento já existente"""
    user = User(username="Test", email="test@test.com", user_password="senha")
    event = Event(
        event_name="Show",
        event_description="Test",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://test.com",
        event_location="SP",
        organizer_id=1
    )
    db.add_all([user, event])
    db.commit()
    
    add_event_user_service(user.user_id, event.event_id, db)
    
    with pytest.raises(ConflictException):
        add_event_user_service(user.user_id, event.event_id, db)


def test_get_user_events_service(db):
    """Testa buscar eventos do usuário"""
    user = User(username="Test", email="test@test.com", user_password="senha")
    db.add(user)
    db.commit()
    
    result = get_user_events_service(user.user_id, db)
    assert result == []


def test_get_user_events_service_not_found(db):
    """Testa buscar eventos de usuário inexistente"""
    with pytest.raises(NotFoundException):
        get_user_events_service(99999, db)


def test_update_user_service(db):
    """Testa atualizar usuário"""
    data = UserCreate(
        username="Antigo",
        email="test@test.com",
        user_password="senha"
    )
    user = create_user_service(data, db)
    
    update = UserUpdate(username="Novo")
    result = update_user_service(user.user_id, update, db)
    
    assert result.username == "Novo"


def test_update_user_service_not_found(db):
    """Testa atualizar usuário inexistente"""
    update = UserUpdate(username="Test")
    
    with pytest.raises(NotFoundException):
        update_user_service(99999, update, db)


def test_delete_user_service(db):
    """Testa deletar usuário"""
    data = UserCreate(
        username="Temp",
        email="temp@test.com",
        user_password="senha"
    )
    user = create_user_service(data, db)
    
    result = delete_user_service(user.user_id, db)
    assert result["message"] == "User deleted successfully!"


def test_delete_user_service_not_found(db):
    """Testa deletar usuário inexistente"""
    with pytest.raises(NotFoundException):
        delete_user_service(99999, db)


def test_delete_genre_user_service(db):
    """Testa remover gênero do usuário"""
    user = User(username="Test", email="test@test.com", user_password="senha")
    genre = Genre(genre_name="Rock")
    db.add_all([user, genre])
    db.commit()
    
    user.genres.append(genre)
    db.commit()
    
    result = delete_genre_user_service(user.user_id, genre.genre_id, db)
    assert result["message"] == "Genre unfavorited successfully!"


def test_delete_genre_user_service_not_found(db):
    """Testa remover gênero de usuário inexistente"""
    with pytest.raises(NotFoundException):
        delete_genre_user_service(99999, 99999, db)


def test_delete_genre_user_service_not_linked(db):
    """Testa remover gênero não vinculado"""
    user = User(username="Test", email="test@test.com", user_password="senha")
    genre = Genre(genre_name="Rock")
    db.add_all([user, genre])
    db.commit()
    
    with pytest.raises(BadRequestException):
        delete_genre_user_service(user.user_id, genre.genre_id, db)
