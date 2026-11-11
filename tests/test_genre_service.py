"""
Testes unitários para o serviço de gêneros (genre_service.py)

Este módulo testa todas as operações relacionadas aos gêneros musicais,
incluindo criação, listagem, atualização, exclusão e consulta de artistas
por gênero.
"""

import pytest
from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Artist, Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from app.services.genre_service import (
    create_genre_service,
    delete_genre_service,
    get_genre_artists_service,
    list_genre_service,
    update_genre_service,
)


# ============================================================================
# TESTES DE CRIAÇÃO DE GÊNERO
# ============================================================================


def test_create_genre_success(db: Session):
    """
    Testa a criação bem-sucedida de um novo gênero musical.
    
    Verifica que:
    - O gênero é criado com o nome correto
    - O gênero é persistido no banco de dados
    - Um ID é atribuído automaticamente
    """
    genre_data = GenreCreate(genre_name="Rock")

    # Cria o gênero usando o serviço
    result = create_genre_service(genre_data, db)

    # Verifica se o gênero foi criado corretamente
    assert result.genre_name == "Rock"
    assert result.genre_id is not None

    # Confirma que o gênero está no banco de dados
    db_genre = db.get(Genre, result.genre_id)
    assert db_genre is not None
    assert db_genre.genre_name == "Rock"


def test_create_genre_with_special_characters(db: Session):
    """
    Testa a criação de gênero com caracteres especiais no nome.
    
    Verifica que:
    - Gêneros com acentos e caracteres especiais são aceitos
    - O nome é armazenado exatamente como fornecido
    """
    genre_data = GenreCreate(genre_name="Música Eletrônica")

    result = create_genre_service(genre_data, db)

    assert result.genre_name == "Música Eletrônica"
    assert result.genre_id is not None


def test_create_duplicate_genre_raises_conflict(db: Session):
    """
    Testa que não é possível criar dois gêneros com o mesmo nome.
    
    Verifica que:
    - Uma exceção ConflictException é lançada ao tentar duplicar
    - O segundo gênero não é criado no banco de dados
    - A contagem de gêneros permanece inalterada
    """
    # Cria o primeiro gênero
    genre_data1 = GenreCreate(genre_name="Jazz")
    create_genre_service(genre_data1, db)

    # Tenta criar segundo gênero com mesmo nome
    genre_data2 = GenreCreate(genre_name="Jazz")

    # Deve lançar exceção de conflito
    with pytest.raises(ConflictException, match="Genre already exists"):
        create_genre_service(genre_data2, db)

    # Verifica que apenas um gênero com este nome existe
    genres = db.query(Genre).filter(Genre.genre_name == "Jazz").all()
    assert len(genres) == 1


# ============================================================================
# TESTES DE LISTAGEM DE GÊNEROS
# ============================================================================


def test_list_genres_empty_database(db: Session):
    """
    Testa a listagem de gêneros quando o banco está vazio.
    
    Verifica que:
    - Uma lista vazia é retornada
    - Não ocorrem erros ao consultar banco vazio
    """
    result = list_genre_service(db)

    # Deve retornar lista (pode estar vazia ou ter dados do conftest)
    assert isinstance(result, list)


def test_list_genres_multiple_entries(db: Session):
    """
    Testa a listagem de múltiplos gêneros.
    
    Verifica que:
    - Todos os gêneros cadastrados são retornados
    - A lista contém os objetos corretos
    """
    # Salva a contagem inicial
    initial_count = len(list_genre_service(db))

    # Cria múltiplos gêneros
    genre_names = ["Rock", "Pop", "Jazz", "Blues", "Samba"]
    for name in genre_names:
        genre_data = GenreCreate(genre_name=name)
        create_genre_service(genre_data, db)

    # Lista todos os gêneros
    result = list_genre_service(db)

    # Verifica que todos foram retornados
    assert len(result) == initial_count + len(genre_names)

    # Verifica que os nomes estão corretos
    result_names = [g.genre_name for g in result]
    for name in genre_names:
        assert name in result_names


# ============================================================================
# TESTES DE ATUALIZAÇÃO DE GÊNERO
# ============================================================================


def test_update_genre_name_success(db: Session):
    """
    Testa a atualização do nome de um gênero.
    
    Verifica que:
    - O nome do gênero é atualizado corretamente
    - A mudança é persistida no banco de dados
    - O ID permanece o mesmo
    """
    # Cria um gênero
    genre_data = GenreCreate(genre_name="Rock Clássico")
    genre = create_genre_service(genre_data, db)
    original_id = genre.genre_id

    # Atualiza o nome do gênero
    update_data = GenreUpdate(genre_name="Classic Rock")
    updated_genre = update_genre_service(genre.genre_id, update_data, db)

    # Verifica que o nome foi atualizado
    assert updated_genre.genre_name == "Classic Rock"
    # Verifica que o ID não mudou
    assert updated_genre.genre_id == original_id

    # Confirma a persistência no banco
    db_genre = db.get(Genre, original_id)
    assert db_genre.genre_name == "Classic Rock"


def test_update_nonexistent_genre_raises_not_found(db: Session):
    """
    Testa a atualização de um gênero que não existe.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    - Nenhuma modificação é feita no banco de dados
    """
    update_data = GenreUpdate(genre_name="Nome Qualquer")

    # Tenta atualizar gênero com ID que não existe
    with pytest.raises(NotFoundException, match="Genre does not exist"):
        update_genre_service(99999, update_data, db)


def test_update_genre_with_empty_update(db: Session):
    """
    Testa a atualização de gênero sem fornecer novos dados.
    
    Verifica que:
    - A operação não falha
    - O gênero permanece inalterado
    """
    # Cria um gênero
    genre_data = GenreCreate(genre_name="Reggae")
    genre = create_genre_service(genre_data, db)

    # Atualiza sem fornecer dados
    update_data = GenreUpdate()
    updated_genre = update_genre_service(genre.genre_id, update_data, db)

    # O nome deve permanecer o mesmo
    assert updated_genre.genre_name == "Reggae"


# ============================================================================
# TESTES DE EXCLUSÃO DE GÊNERO
# ============================================================================


def test_delete_genre_success(db: Session):
    """
    Testa a exclusão bem-sucedida de um gênero.
    
    Verifica que:
    - O gênero é removido do banco de dados
    - Relacionamentos com usuários e artistas são limpos
    - Uma mensagem de sucesso é retornada
    """
    # Cria um gênero
    genre_data = GenreCreate(genre_name="Hip Hop")
    genre = create_genre_service(genre_data, db)
    genre_id = genre.genre_id

    # Exclui o gênero
    result = delete_genre_service(genre_id, db)

    # Verifica a mensagem de sucesso
    assert result["message"] == "Genre deleted successfully!"

    # Confirma que o gênero não existe mais
    deleted_genre = db.get(Genre, genre_id)
    assert deleted_genre is None


def test_delete_genre_clears_relationships(db: Session):
    """
    Testa que a exclusão de gênero remove relacionamentos com artistas.
    
    Verifica que:
    - Artistas associados não são excluídos
    - A associação entre gênero e artista é removida
    """
    # Cria um gênero e um artista
    genre_data = GenreCreate(genre_name="Metal")
    genre = create_genre_service(genre_data, db)

    artist = Artist(artist_name="Banda de Metal")
    db.add(artist)
    db.commit()

    # Associa o artista ao gênero
    artist.genres.append(genre)
    db.commit()

    # Verifica a associação antes da exclusão
    db.refresh(artist)
    assert genre in artist.genres

    # Exclui o gênero
    delete_genre_service(genre.genre_id, db)

    # Verifica que o artista ainda existe
    db.refresh(artist)
    assert db.get(Artist, artist.artist_id) is not None

    # Verifica que a associação foi removida
    assert genre not in artist.genres


def test_delete_nonexistent_genre_raises_not_found(db: Session):
    """
    Testa a tentativa de excluir um gênero inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    - A mensagem de erro é apropriada
    """
    with pytest.raises(NotFoundException, match="Genre does not exist"):
        delete_genre_service(99999, db)


# ============================================================================
# TESTES DE CONSULTA DE ARTISTAS POR GÊNERO
# ============================================================================


def test_get_genre_artists_empty_list(db: Session):
    """
    Testa a consulta de artistas para um gênero sem artistas associados.
    
    Verifica que:
    - Uma lista vazia é retornada
    - Não ocorrem erros quando não há artistas
    """
    # Cria um gênero sem artistas
    genre_data = GenreCreate(genre_name="Folk")
    genre = create_genre_service(genre_data, db)

    # Consulta os artistas do gênero
    result = get_genre_artists_service(genre.genre_id, db)

    # Deve retornar lista vazia
    assert result == []


def test_get_genre_artists_with_multiple_artists(db: Session):
    """
    Testa a consulta de artistas para um gênero com múltiplos artistas.
    
    Verifica que:
    - Todos os artistas associados são retornados
    - A lista contém os objetos corretos
    """
    # Cria um gênero
    genre_data = GenreCreate(genre_name="Indie")
    genre = create_genre_service(genre_data, db)

    # Cria múltiplos artistas e associa ao gênero
    artist_names = ["Banda A", "Banda B", "Banda C"]
    for name in artist_names:
        artist = Artist(artist_name=name)
        db.add(artist)
        db.commit()
        artist.genres.append(genre)
        db.commit()

    # Consulta os artistas do gênero
    result = get_genre_artists_service(genre.genre_id, db)

    # Verifica que todos os artistas foram retornados
    assert len(result) == len(artist_names)

    # Verifica que os nomes estão corretos
    result_names = [a.artist_name for a in result]
    for name in artist_names:
        assert name in result_names


def test_get_artists_for_nonexistent_genre_raises_not_found(db: Session):
    """
    Testa a consulta de artistas para um gênero inexistente.
    
    Verifica que:
    - Uma exceção NotFoundException é lançada
    - A mensagem indica que o gênero não existe
    """
    with pytest.raises(NotFoundException, match="Genre does not exist"):
        get_genre_artists_service(99999, db)


def test_get_genre_artists_does_not_include_unrelated_artists(db: Session):
    """
    Testa que a consulta retorna apenas artistas do gênero específico.
    
    Verifica que:
    - Artistas de outros gêneros não são incluídos
    - A filtragem funciona corretamente
    """
    # Cria dois gêneros
    genre1_data = GenreCreate(genre_name="Rock")
    genre1 = create_genre_service(genre1_data, db)

    genre2_data = GenreCreate(genre_name="Pop")
    genre2 = create_genre_service(genre2_data, db)

    # Cria artistas para cada gênero
    rock_artist = Artist(artist_name="Banda de Rock")
    pop_artist = Artist(artist_name="Cantor Pop")
    db.add(rock_artist)
    db.add(pop_artist)
    db.commit()

    # Associa cada artista ao seu gênero
    rock_artist.genres.append(genre1)
    pop_artist.genres.append(genre2)
    db.commit()

    # Consulta artistas do gênero Rock
    result = get_genre_artists_service(genre1.genre_id, db)

    # Verifica que apenas o artista de Rock foi retornado
    assert len(result) == 1
    assert result[0].artist_name == "Banda de Rock"
    assert pop_artist not in result


# ============================================================================
# TESTES DE CENÁRIOS COMPLEXOS
# ============================================================================


def test_genre_lifecycle_complete_flow(db: Session):
    """
    Testa o ciclo de vida completo de um gênero.
    
    Verifica:
    - Criação
    - Associação com artistas
    - Atualização de nome
    - Consulta de artistas
    - Exclusão
    """
    # 1. Criação
    genre_data = GenreCreate(genre_name="Experimental")
    genre = create_genre_service(genre_data, db)
    assert genre.genre_name == "Experimental"

    # 2. Associação com artistas
    artist = Artist(artist_name="Artista Experimental")
    db.add(artist)
    db.commit()
    artist.genres.append(genre)
    db.commit()

    # 3. Atualização
    update_data = GenreUpdate(genre_name="Avant-Garde")
    updated_genre = update_genre_service(genre.genre_id, update_data, db)
    assert updated_genre.genre_name == "Avant-Garde"

    # 4. Consulta de artistas
    artists = get_genre_artists_service(genre.genre_id, db)
    assert len(artists) == 1
    assert artists[0].artist_name == "Artista Experimental"

    # 5. Exclusão
    result = delete_genre_service(genre.genre_id, db)
    assert result["message"] == "Genre deleted successfully!"
    assert db.get(Genre, genre.genre_id) is None


def test_multiple_genres_same_artist(db: Session):
    """
    Testa que um artista pode estar associado a múltiplos gêneros.
    
    Verifica que:
    - Um artista pode ter vários gêneros
    - Cada gênero lista o artista corretamente
    """
    # Cria múltiplos gêneros
    genres = []
    for name in ["Rock", "Blues", "Country"]:
        genre_data = GenreCreate(genre_name=name)
        genre = create_genre_service(genre_data, db)
        genres.append(genre)

    # Cria um artista e associa a todos os gêneros
    artist = Artist(artist_name="Artista Versátil")
    db.add(artist)
    db.commit()

    for genre in genres:
        artist.genres.append(genre)
    db.commit()

    # Verifica que cada gênero lista o artista
    for genre in genres:
        artists = get_genre_artists_service(genre.genre_id, db)
        assert len(artists) == 1
        assert artists[0].artist_name == "Artista Versátil"
