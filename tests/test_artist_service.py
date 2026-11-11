"""
Testes unitários para o serviço de artistas (artist_service.py)

Este módulo testa todas as operações relacionadas aos artistas,
incluindo criação, listagem, atualização, exclusão e gerenciamento
de relacionamentos com gêneros musicais e eventos.
"""

import pytest
from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.exceptions.ValidationException import ValidationException
from app.models import Artist, Event, Genre
from app.schemas.artist import ArtistCreate, ArtistUpdate
from app.services.artist_service import (
    add_genre_artist_service,
    create_artist_service,
    delete_artist_service,
    get_artist_events_service,
    list_artists_service,
    remove_artist_genres_service,
    update_artist_service,
)


# ============================================================================
# TESTES DE CRIAÇÃO DE ARTISTA
# ============================================================================


def test_create_artist_without_genres(db: Session):
    """
    Testa a criação de um artista sem gêneros associados.
    
    Verifica que:
    - O artista é criado com nome correto
    - spotify_id pode ser None
    - O artista é persistido no banco de dados
    """
    artist_data = ArtistCreate(artist_name="Banda Nova", spotify_id=None, genres=[])

    result = create_artist_service(artist_data, db)

    assert result.artist_name == "Banda Nova"
    assert result.spotify_id is None
    assert result.artist_id is not None

    # Confirma que está no banco
    db_artist = db.get(Artist, result.artist_id)
    assert db_artist is not None
    assert db_artist.artist_name == "Banda Nova"


def test_create_artist_with_spotify_id(db: Session):
    """
    Testa a criação de artista com ID do Spotify.
    
    Verifica que:
    - O spotify_id é armazenado corretamente
    - Permite integração com a API do Spotify
    """
    artist_data = ArtistCreate(
        artist_name="Artista Spotify", spotify_id="spotify123", genres=[]
    )

    result = create_artist_service(artist_data, db)

    assert result.artist_name == "Artista Spotify"
    assert result.spotify_id == "spotify123"


def test_create_artist_with_genres(db: Session):
    """
    Testa a criação de artista já associado a gêneros musicais.
    
    Verifica que:
    - Os gêneros são associados ao artista na criação
    - A lista de gêneros pode conter múltiplos itens
    """
    # Cria gêneros primeiro
    rock = Genre(genre_name="Rock")
    blues = Genre(genre_name="Blues")
    db.add_all([rock, blues])
    db.commit()

    # Cria artista com gêneros
    artist_data = ArtistCreate(
        artist_name="Banda Rock Blues", spotify_id=None, genres=["Rock", "Blues"]
    )

    result = create_artist_service(artist_data, db)

    assert result.artist_name == "Banda Rock Blues"
    assert len(result.genres) == 2
    genre_names = [g.genre_name for g in result.genres]
    assert "Rock" in genre_names
    assert "Blues" in genre_names


def test_create_artist_with_nonexistent_genre_raises_not_found(db: Session):
    """
    Testa a criação de artista com gênero que não existe.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    - O artista não é criado no banco de dados
    """
    artist_data = ArtistCreate(
        artist_name="Artista Problema", spotify_id=None, genres=["GêneroInexistente"]
    )

    with pytest.raises(
        NotFoundException, match="Genre 'GêneroInexistente' does not exist"
    ):
        create_artist_service(artist_data, db)


def test_create_artist_duplicate_spotify_id_raises_conflict(db: Session):
    """
    Testa que não é possível criar dois artistas com mesmo spotify_id.
    
    Verifica que:
    - Uma exceção ConflictException é lançada
    - Apenas um artista com aquele spotify_id existe
    """
    # Cria primeiro artista
    artist1 = ArtistCreate(
        artist_name="Artista Original", spotify_id="uniqueId123", genres=[]
    )
    create_artist_service(artist1, db)

    # Tenta criar segundo com mesmo spotify_id
    artist2 = ArtistCreate(
        artist_name="Artista Duplicado", spotify_id="uniqueId123", genres=[]
    )

    with pytest.raises(ConflictException, match="Spotify artist already exists"):
        create_artist_service(artist2, db)


# ============================================================================
# TESTES DE LISTAGEM DE ARTISTAS
# ============================================================================


def test_list_artists_empty_database(db: Session):
    """
    Testa a listagem quando não há artistas cadastrados.
    
    Verifica que:
    - Uma lista é retornada (pode estar vazia ou ter dados do conftest)
    - Não ocorrem erros
    """
    result = list_artists_service(db)
    assert isinstance(result, list)


def test_list_artists_multiple_entries(db: Session):
    """
    Testa a listagem com múltiplos artistas cadastrados.
    
    Verifica que:
    - Todos os artistas são retornados
    - Os dados estão completos e corretos
    """
    initial_count = len(list_artists_service(db))

    # Cria múltiplos artistas
    artist_names = ["Banda A", "Banda B", "Banda C"]
    for name in artist_names:
        artist_data = ArtistCreate(artist_name=name, spotify_id=None, genres=[])
        create_artist_service(artist_data, db)

    result = list_artists_service(db)

    assert len(result) == initial_count + len(artist_names)

    # Verifica que os nomes estão presentes
    result_names = [a.artist_name for a in result]
    for name in artist_names:
        assert name in result_names


# ============================================================================
# TESTES DE ATUALIZAÇÃO DE ARTISTA
# ============================================================================


def test_update_artist_name(db: Session):
    """
    Testa a atualização do nome de um artista.
    
    Verifica que:
    - O nome é atualizado corretamente
    - Outros campos permanecem inalterados
    """
    # Cria artista
    artist_data = ArtistCreate(artist_name="Nome Antigo", spotify_id=None, genres=[])
    artist = create_artist_service(artist_data, db)

    # Atualiza o nome
    update_data = ArtistUpdate(artist_name="Nome Novo")
    updated = update_artist_service(artist.artist_id, update_data, db)

    assert updated.artist_name == "Nome Novo"
    assert updated.artist_id == artist.artist_id


def test_update_artist_spotify_id(db: Session):
    """
    Testa a atualização do spotify_id de um artista.
    
    Verifica que:
    - O spotify_id é atualizado corretamente
    - Permite vincular artista local ao Spotify posteriormente
    """
    # Cria artista sem spotify_id
    artist_data = ArtistCreate(artist_name="Banda Local", spotify_id=None, genres=[])
    artist = create_artist_service(artist_data, db)

    # Adiciona spotify_id
    update_data = ArtistUpdate(spotify_id="newSpotifyId456")
    updated = update_artist_service(artist.artist_id, update_data, db)

    assert updated.spotify_id == "newSpotifyId456"
    assert updated.artist_name == "Banda Local"


def test_update_artist_spotify_id_conflict(db: Session):
    """
    Testa que não é possível atualizar para um spotify_id já existente.
    
    Verifica que:
    - Uma exceção ConflictException é lançada
    - O spotify_id não é alterado
    """
    # Cria dois artistas
    artist1_data = ArtistCreate(
        artist_name="Artista 1", spotify_id="spotify111", genres=[]
    )
    artist1 = create_artist_service(artist1_data, db)

    artist2_data = ArtistCreate(
        artist_name="Artista 2", spotify_id="spotify222", genres=[]
    )
    artist2 = create_artist_service(artist2_data, db)

    # Tenta atualizar artista2 com spotify_id do artista1
    update_data = ArtistUpdate(spotify_id="spotify111")

    with pytest.raises(ConflictException, match="Spotify artist already exists"):
        update_artist_service(artist2.artist_id, update_data, db)


def test_update_nonexistent_artist_raises_not_found(db: Session):
    """
    Testa a atualização de um artista que não existe.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    """
    update_data = ArtistUpdate(artist_name="Qualquer Nome")

    with pytest.raises(NotFoundException, match="Artist does not exist"):
        update_artist_service(99999, update_data, db)


# ============================================================================
# TESTES DE EXCLUSÃO DE ARTISTA
# ============================================================================


def test_delete_artist_success(db: Session):
    """
    Testa a exclusão bem-sucedida de um artista.
    
    Verifica que:
    - O artista é removido do banco
    - Relacionamentos com gêneros são limpos
    - Mensagem de sucesso é retornada
    """
    # Cria artista
    artist_data = ArtistCreate(artist_name="Banda Temporária", genres=[])
    artist = create_artist_service(artist_data, db)
    artist_id = artist.artist_id

    # Exclui
    result = delete_artist_service(artist_id, db)

    assert result["message"] == "Arists deleted successfully!"

    # Confirma exclusão
    deleted = db.get(Artist, artist_id)
    assert deleted is None


def test_delete_artist_clears_genre_relationships(db: Session):
    """
    Testa que a exclusão de artista remove associações com gêneros.
    
    Verifica que:
    - Gêneros associados não são excluídos
    - Apenas a associação é removida
    """
    # Cria gênero e artista
    genre = Genre(genre_name="Metal")
    db.add(genre)
    db.commit()

    artist_data = ArtistCreate(
        artist_name="Banda Metal", spotify_id=None, genres=["Metal"]
    )
    artist = create_artist_service(artist_data, db)

    # Verifica associação antes da exclusão
    db.refresh(genre)
    assert artist in genre.artists

    # Exclui artista
    delete_artist_service(artist.artist_id, db)

    # Verifica que gênero ainda existe
    db.refresh(genre)
    assert db.get(Genre, genre.genre_id) is not None

    # Verifica que associação foi removida
    assert artist not in genre.artists


def test_delete_nonexistent_artist_raises_not_found(db: Session):
    """
    Testa a tentativa de excluir um artista inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    """
    with pytest.raises(NotFoundException, match="Artist does not exist"):
        delete_artist_service(99999, db)


# ============================================================================
# TESTES DE GERENCIAMENTO DE GÊNEROS DO ARTISTA
# ============================================================================


def test_add_genre_to_artist_success(db: Session):
    """
    Testa a adição de um gênero a um artista.
    
    Verifica que:
    - O gênero é associado ao artista
    - O artista atualizado é retornado
    """
    # Cria artista e gênero
    artist_data = ArtistCreate(artist_name="Banda Versátil", genres=[])
    artist = create_artist_service(artist_data, db)

    genre = Genre(genre_name="Funk")
    db.add(genre)
    db.commit()

    # Adiciona gênero ao artista
    result = add_genre_artist_service(artist.artist_id, genre.genre_id, db)

    assert genre in result.genres
    assert result.artist_name == "Banda Versátil"


def test_add_duplicate_genre_to_artist_raises_conflict(db: Session):
    """
    Testa a tentativa de adicionar um gênero já associado ao artista.
    
    Verifica que:
    - Uma exceção ConflictException é lançada
    - O gênero não é duplicado
    """
    # Cria artista com um gênero
    genre = Genre(genre_name="Samba")
    db.add(genre)
    db.commit()

    artist_data = ArtistCreate(
        artist_name="Sambista", spotify_id=None, genres=["Samba"]
    )
    artist = create_artist_service(artist_data, db)

    # Tenta adicionar o mesmo gênero novamente
    with pytest.raises(ConflictException, match="Genre already linked to Artist"):
        add_genre_artist_service(artist.artist_id, genre.genre_id, db)


def test_add_genre_to_nonexistent_artist_raises_not_found(db: Session):
    """
    Testa a adição de gênero a um artista inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    """
    genre = Genre(genre_name="Country")
    db.add(genre)
    db.commit()

    with pytest.raises(NotFoundException, match="Artist or Genre does not exist"):
        add_genre_artist_service(99999, genre.genre_id, db)


def test_add_nonexistent_genre_to_artist_raises_not_found(db: Session):
    """
    Testa a adição de um gênero inexistente a um artista.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    """
    artist_data = ArtistCreate(artist_name="Artista Qualquer", genres=[])
    artist = create_artist_service(artist_data, db)

    with pytest.raises(NotFoundException, match="Artist or Genre does not exist"):
        add_genre_artist_service(artist.artist_id, 99999, db)


def test_remove_genre_from_artist_success(db: Session):
    """
    Testa a remoção de um gênero de um artista.
    
    Verifica que:
    - O gênero é removido da lista do artista
    - Mensagem de sucesso é retornada
    """
    # Cria artista com gênero
    genre = Genre(genre_name="Reggae")
    db.add(genre)
    db.commit()

    artist_data = ArtistCreate(
        artist_name="Banda Reggae", spotify_id=None, genres=["Reggae"]
    )
    artist = create_artist_service(artist_data, db)

    # Remove o gênero
    result = remove_artist_genres_service(artist.artist_id, genre.genre_id, db)

    assert result["message"] == "Artist removed from Genre successfully!"

    # Confirma remoção
    db.refresh(artist)
    assert genre not in artist.genres


def test_remove_unlinked_genre_raises_validation_exception(db: Session):
    """
    Testa a remoção de um gênero não associado ao artista.
    
    Verifica que:
    - Uma exceção ValidationException é lançada
    """
    # Cria artista e gênero separadamente (não associados)
    artist_data = ArtistCreate(artist_name="Banda Independente", genres=[])
    artist = create_artist_service(artist_data, db)

    genre = Genre(genre_name="Eletrônica")
    db.add(genre)
    db.commit()

    # Tenta remover gênero não associado
    with pytest.raises(
        ValidationException, match="Genre not linked to this Artist"
    ):
        remove_artist_genres_service(artist.artist_id, genre.genre_id, db)


# ============================================================================
# TESTES DE CONSULTA DE EVENTOS DO ARTISTA
# ============================================================================


def test_get_artist_events_empty_list(db: Session):
    """
    Testa a consulta de eventos para um artista sem eventos.
    
    Verifica que:
    - Uma lista vazia é retornada
    - Não ocorrem erros
    """
    artist_data = ArtistCreate(artist_name="Artista Sem Shows", genres=[])
    artist = create_artist_service(artist_data, db)

    result = get_artist_events_service(artist.artist_id, db)

    assert result == []


def test_get_artist_events_with_multiple_events(db: Session):
    """
    Testa a consulta de eventos para um artista com múltiplos shows.
    
    Verifica que:
    - Todos os eventos do artista são retornados
    - A lista está completa
    """
    from datetime import date, timedelta

    # Cria artista
    artist_data = ArtistCreate(artist_name="Banda Famosa", genres=[])
    artist = create_artist_service(artist_data, db)

    # Cria múltiplos eventos com este artista
    for i in range(3):
        event = Event(
            event_name=f"Show {i}",
            event_description=f"Descrição {i}",
            event_date=date.today() + timedelta(days=10 + i),
            ticket_link=f"https://example.com/show{i}",
            event_location="São Paulo",
            organizer_id=1,  # Organizador do conftest
        )
        db.add(event)
        db.commit()
        event.artists.append(artist)
        db.commit()

    # Consulta os eventos
    result = get_artist_events_service(artist.artist_id, db)

    assert len(result) == 3
    event_names = [e.event_name for e in result]
    assert "Show 0" in event_names
    assert "Show 1" in event_names
    assert "Show 2" in event_names


def test_get_events_for_nonexistent_artist_raises_not_found(db: Session):
    """
    Testa a consulta de eventos para um artista inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    """
    with pytest.raises(NotFoundException, match="Artist does not exist"):
        get_artist_events_service(99999, db)


# ============================================================================
# TESTES DE CENÁRIOS COMPLEXOS
# ============================================================================


def test_artist_lifecycle_complete_flow(db: Session):
    """
    Testa o ciclo de vida completo de um artista.
    
    Verifica:
    - Criação sem gêneros
    - Adição de gêneros
    - Atualização de dados
    - Consulta de relacionamentos
    - Exclusão
    """
    # 1. Criação
    artist_data = ArtistCreate(artist_name="Artista Teste", genres=[])
    artist = create_artist_service(artist_data, db)
    assert artist.artist_name == "Artista Teste"

    # 2. Adição de gêneros
    genre1 = Genre(genre_name="Rock")
    genre2 = Genre(genre_name="Pop")
    db.add_all([genre1, genre2])
    db.commit()

    add_genre_artist_service(artist.artist_id, genre1.genre_id, db)
    add_genre_artist_service(artist.artist_id, genre2.genre_id, db)

    db.refresh(artist)
    assert len(artist.genres) == 2

    # 3. Atualização
    update_data = ArtistUpdate(
        artist_name="Artista Teste Atualizado", spotify_id="spotifyTest123"
    )
    updated = update_artist_service(artist.artist_id, update_data, db)
    assert updated.artist_name == "Artista Teste Atualizado"
    assert updated.spotify_id == "spotifyTest123"

    # 4. Consulta de eventos (deve estar vazio)
    events = get_artist_events_service(artist.artist_id, db)
    assert events == []

    # 5. Exclusão
    result = delete_artist_service(artist.artist_id, db)
    assert result["message"] == "Arists deleted successfully!"
    assert db.get(Artist, artist.artist_id) is None


def test_multiple_artists_same_genre(db: Session):
    """
    Testa que múltiplos artistas podem compartilhar o mesmo gênero.
    
    Verifica que:
    - Um gênero pode estar associado a vários artistas
    - As associações são independentes
    """
    # Cria um gênero
    genre = Genre(genre_name="Jazz")
    db.add(genre)
    db.commit()

    # Cria múltiplos artistas com este gênero
    artists = []
    for i in range(3):
        artist_data = ArtistCreate(
            artist_name=f"Jazzista {i}", spotify_id=None, genres=["Jazz"]
        )
        artist = create_artist_service(artist_data, db)
        artists.append(artist)

    # Verifica que todos estão associados ao gênero
    db.refresh(genre)
    assert len(genre.artists) == 3

    for artist in artists:
        assert genre in artist.genres
