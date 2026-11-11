"""
Testes CRUD Básicos - Versão Simplificada

Testes simples e diretos para operações básicas de Create, Read, Update e Delete.
Ideal para entender o funcionamento básico dos serviços.
"""

import pytest
from datetime import date, timedelta

from app.models import Artist, Event, Genre, Organizer, User


# ============================================================================
# TESTES BÁSICOS DE GÊNERO
# ============================================================================


def test_criar_genero(db):
    """
    Teste básico: Criar um gênero e verificar se foi salvo.
    """
    # Cria um gênero
    genero = Genre(genre_name="Rock")
    db.add(genero)
    db.commit()

    # Verifica se foi criado
    assert genero.genre_id is not None
    assert genero.genre_name == "Rock"


def test_buscar_genero_por_id(db):
    """
    Teste básico: Buscar um gênero pelo ID.
    """
    # Cria e salva
    genero = Genre(genre_name="Pop")
    db.add(genero)
    db.commit()

    # Busca pelo ID
    genero_encontrado = db.get(Genre, genero.genre_id)

    # Verifica
    assert genero_encontrado is not None
    assert genero_encontrado.genre_name == "Pop"


def test_atualizar_genero(db):
    """
    Teste básico: Atualizar o nome de um gênero.
    """
    # Cria um gênero
    genero = Genre(genre_name="Rap")
    db.add(genero)
    db.commit()

    # Atualiza o nome
    genero.genre_name = "Hip Hop"
    db.commit()

    # Verifica a atualização
    db.refresh(genero)
    assert genero.genre_name == "Hip Hop"


def test_deletar_genero(db):
    """
    Teste básico: Deletar um gênero.
    """
    # Cria um gênero
    genero = Genre(genre_name="Blues")
    db.add(genero)
    db.commit()
    genero_id = genero.genre_id

    # Delete o gênero
    db.delete(genero)
    db.commit()

    # Verifica que foi deletado
    genero_deletado = db.get(Genre, genero_id)
    assert genero_deletado is None


def test_listar_todos_generos(db):
    """
    Teste básico: Listar todos os gêneros cadastrados.
    """
    # Cria alguns gêneros
    db.add(Genre(genre_name="Rock"))
    db.add(Genre(genre_name="Jazz"))
    db.add(Genre(genre_name="Samba"))
    db.commit()

    # Lista todos
    todos_generos = db.query(Genre).all()

    # Verifica que tem pelo menos 3
    assert len(todos_generos) >= 3


# ============================================================================
# TESTES BÁSICOS DE ARTISTA
# ============================================================================


def test_criar_artista(db):
    """
    Teste básico: Criar um artista.
    """
    artista = Artist(artist_name="Beatles")
    db.add(artista)
    db.commit()

    assert artista.artist_id is not None
    assert artista.artist_name == "Beatles"


def test_criar_artista_com_spotify_id(db):
    """
    Teste básico: Criar artista com ID do Spotify.
    """
    artista = Artist(artist_name="Queen", spotify_id="spotify123")
    db.add(artista)
    db.commit()

    assert artista.spotify_id == "spotify123"


def test_buscar_artista_por_nome(db):
    """
    Teste básico: Buscar artista pelo nome.
    """
    # Cria artista
    artista = Artist(artist_name="Pink Floyd")
    db.add(artista)
    db.commit()

    # Busca pelo nome
    encontrado = db.query(Artist).filter(Artist.artist_name == "Pink Floyd").first()

    assert encontrado is not None
    assert encontrado.artist_name == "Pink Floyd"


def test_atualizar_nome_artista(db):
    """
    Teste básico: Atualizar nome do artista.
    """
    artista = Artist(artist_name="Nome Antigo")
    db.add(artista)
    db.commit()

    # Atualiza
    artista.artist_name = "Nome Novo"
    db.commit()

    db.refresh(artista)
    assert artista.artist_name == "Nome Novo"


def test_deletar_artista(db):
    """
    Teste básico: Deletar artista.
    """
    artista = Artist(artist_name="Artista Temporário")
    db.add(artista)
    db.commit()
    artista_id = artista.artist_id

    db.delete(artista)
    db.commit()

    assert db.get(Artist, artista_id) is None


def test_contar_artistas(db):
    """
    Teste básico: Contar quantos artistas existem.
    """
    # Conta inicial
    contagem_inicial = db.query(Artist).count()

    # Adiciona 2 artistas
    db.add(Artist(artist_name="Artista 1"))
    db.add(Artist(artist_name="Artista 2"))
    db.commit()

    # Conta novamente
    contagem_final = db.query(Artist).count()

    assert contagem_final == contagem_inicial + 2


# ============================================================================
# TESTES BÁSICOS DE USUÁRIO
# ============================================================================


def test_criar_usuario(db):
    """
    Teste básico: Criar um usuário.
    """
    usuario = User(
        username="João",
        email="joao@teste.com",
        user_password="senha123"
    )
    db.add(usuario)
    db.commit()

    assert usuario.user_id is not None
    assert usuario.username == "João"
    assert usuario.email == "joao@teste.com"


def test_buscar_usuario_por_email(db):
    """
    Teste básico: Buscar usuário pelo email.
    """
    usuario = User(
        username="Maria",
        email="maria@teste.com",
        user_password="senha456"
    )
    db.add(usuario)
    db.commit()

    # Busca
    encontrado = db.query(User).filter(User.email == "maria@teste.com").first()

    assert encontrado is not None
    assert encontrado.username == "Maria"


def test_atualizar_username(db):
    """
    Teste básico: Atualizar nome de usuário.
    """
    usuario = User(
        username="Pedro",
        email="pedro@teste.com",
        user_password="senha789"
    )
    db.add(usuario)
    db.commit()

    # Atualiza
    usuario.username = "Pedro Silva"
    db.commit()

    db.refresh(usuario)
    assert usuario.username == "Pedro Silva"


def test_deletar_usuario(db):
    """
    Teste básico: Deletar usuário.
    """
    usuario = User(
        username="Temp",
        email="temp@teste.com",
        user_password="senha000"
    )
    db.add(usuario)
    db.commit()
    usuario_id = usuario.user_id

    db.delete(usuario)
    db.commit()

    assert db.get(User, usuario_id) is None


def test_usuario_campos_opcionais(db):
    """
    Teste básico: Criar usuário com campos opcionais vazios.
    """
    usuario = User(
        username="Ana",
        email="ana@teste.com",
        user_password="senha321",
        profile_image="",
        country=""
    )
    db.add(usuario)
    db.commit()

    assert usuario.profile_image == ""
    assert usuario.country == ""


# ============================================================================
# TESTES BÁSICOS DE EVENTO
# ============================================================================


def test_criar_evento(db):
    """
    Teste básico: Criar um evento.
    """
    # Cria um organizador primeiro (necessário para o evento)
    organizador = Organizer(organizer_name="Produtora XYZ")
    db.add(organizador)
    db.commit()

    # Cria o evento
    evento = Event(
        event_name="Rock in Rio",
        event_description="Festival de música",
        event_date=date.today() + timedelta(days=30),
        ticket_link="https://tickets.com",
        event_location="Rio de Janeiro",
        organizer_id=organizador.organizer_id
    )
    db.add(evento)
    db.commit()

    assert evento.event_id is not None
    assert evento.event_name == "Rock in Rio"


def test_buscar_evento_por_nome(db):
    """
    Teste básico: Buscar evento pelo nome.
    """
    evento = Event(
        event_name="Lollapalooza",
        event_description="Festival",
        event_date=date.today() + timedelta(days=60),
        ticket_link="https://lolla.com",
        event_location="São Paulo",
        organizer_id=1  # Organizador do conftest
    )
    db.add(evento)
    db.commit()

    # Busca
    encontrado = db.query(Event).filter(Event.event_name == "Lollapalooza").first()

    assert encontrado is not None
    assert encontrado.event_location == "São Paulo"


def test_atualizar_descricao_evento(db):
    """
    Teste básico: Atualizar descrição do evento.
    """
    evento = Event(
        event_name="Show Teste",
        event_description="Descrição antiga",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://show.com",
        event_location="Brasília",
        organizer_id=1
    )
    db.add(evento)
    db.commit()

    # Atualiza descrição
    evento.event_description = "Nova descrição atualizada"
    db.commit()

    db.refresh(evento)
    assert evento.event_description == "Nova descrição atualizada"


def test_deletar_evento(db):
    """
    Teste básico: Deletar evento.
    """
    evento = Event(
        event_name="Evento Temporário",
        event_description="Teste",
        event_date=date.today() + timedelta(days=5),
        ticket_link="https://temp.com",
        event_location="Local",
        organizer_id=1
    )
    db.add(evento)
    db.commit()
    evento_id = evento.event_id

    db.delete(evento)
    db.commit()

    assert db.get(Event, evento_id) is None


def test_evento_com_coordenadas(db):
    """
    Teste básico: Criar evento com coordenadas geográficas.
    """
    evento = Event(
        event_name="Show Localizado",
        event_description="Com GPS",
        event_date=date.today() + timedelta(days=15),
        ticket_link="https://gps.com",
        event_location="São Paulo",
        organizer_id=1,
        latitude=-23.5505,
        longitude=-46.6333
    )
    db.add(evento)
    db.commit()

    assert evento.latitude == -23.5505
    assert evento.longitude == -46.6333


# ============================================================================
# TESTES BÁSICOS DE RELACIONAMENTOS
# ============================================================================


def test_adicionar_genero_ao_artista(db):
    """
    Teste básico: Associar um gênero a um artista.
    """
    # Cria gênero e artista
    genero = Genre(genre_name="Rock")
    artista = Artist(artist_name="AC/DC")
    
    db.add(genero)
    db.add(artista)
    db.commit()

    # Associa
    artista.genres.append(genero)
    db.commit()

    # Verifica
    db.refresh(artista)
    assert genero in artista.genres
    assert len(artista.genres) == 1


def test_adicionar_artista_ao_evento(db):
    """
    Teste básico: Associar artista a um evento.
    """
    # Cria artista e evento
    artista = Artist(artist_name="Metallica")
    evento = Event(
        event_name="Metal Festival",
        event_description="Festival de metal",
        event_date=date.today() + timedelta(days=20),
        ticket_link="https://metal.com",
        event_location="Local",
        organizer_id=1
    )
    
    db.add(artista)
    db.add(evento)
    db.commit()

    # Associa artista ao evento
    evento.artists.append(artista)
    db.commit()

    # Verifica
    db.refresh(evento)
    assert artista in evento.artists
    assert len(evento.artists) == 1


def test_adicionar_genero_ao_usuario(db):
    """
    Teste básico: Adicionar gênero preferido ao usuário.
    """
    # Cria usuário e gênero
    usuario = User(
        username="Carlos",
        email="carlos@teste.com",
        user_password="senha999"
    )
    genero = Genre(genre_name="Jazz")
    
    db.add(usuario)
    db.add(genero)
    db.commit()

    # Adiciona gênero às preferências
    usuario.genres.append(genero)
    db.commit()

    # Verifica
    db.refresh(usuario)
    assert genero in usuario.genres
    assert len(usuario.genres) == 1


def test_remover_genero_do_artista(db):
    """
    Teste básico: Remover gênero de um artista.
    """
    # Cria e associa
    genero = Genre(genre_name="Pop")
    artista = Artist(artist_name="Madonna")
    
    db.add(genero)
    db.add(artista)
    db.commit()
    
    artista.genres.append(genero)
    db.commit()

    # Remove
    artista.genres.remove(genero)
    db.commit()

    # Verifica
    db.refresh(artista)
    assert genero not in artista.genres
    assert len(artista.genres) == 0


def test_artista_com_multiplos_generos(db):
    """
    Teste básico: Artista pode ter múltiplos gêneros.
    """
    # Cria artista e 3 gêneros
    artista = Artist(artist_name="David Bowie")
    genero1 = Genre(genre_name="Rock")
    genero2 = Genre(genre_name="Pop")
    genero3 = Genre(genre_name="Glam")
    
    db.add(artista)
    db.add_all([genero1, genero2, genero3])
    db.commit()

    # Adiciona todos os gêneros
    artista.genres.extend([genero1, genero2, genero3])
    db.commit()

    # Verifica
    db.refresh(artista)
    assert len(artista.genres) == 3


# ============================================================================
# TESTES BÁSICOS DE QUERIES
# ============================================================================


def test_filtrar_artistas_por_genero(db):
    """
    Teste básico: Buscar todos os artistas de um gênero.
    """
    # Cria gênero e artistas
    rock = Genre(genre_name="Rock")
    artista1 = Artist(artist_name="Led Zeppelin")
    artista2 = Artist(artist_name="Rolling Stones")
    
    db.add(rock)
    db.add(artista1)
    db.add(artista2)
    db.commit()

    # Associa ambos ao Rock
    artista1.genres.append(rock)
    artista2.genres.append(rock)
    db.commit()

    # Busca artistas desse gênero
    db.refresh(rock)
    artistas_rock = rock.artists

    assert len(artistas_rock) == 2


def test_buscar_eventos_futuros(db):
    """
    Teste básico: Buscar apenas eventos futuros.
    """
    # Cria evento futuro
    evento_futuro = Event(
        event_name="Evento Futuro",
        event_description="Teste",
        event_date=date.today() + timedelta(days=30),
        ticket_link="https://futuro.com",
        event_location="Local",
        organizer_id=1
    )
    db.add(evento_futuro)
    db.commit()

    # Busca eventos futuros
    eventos = db.query(Event).filter(Event.event_date > date.today()).all()

    assert len(eventos) >= 1
    assert evento_futuro in eventos


def test_contar_usuarios_por_genero(db):
    """
    Teste básico: Contar quantos usuários gostam de um gênero.
    """
    # Cria gênero
    samba = Genre(genre_name="Samba")
    db.add(samba)
    db.commit()

    # Cria 3 usuários que gostam de Samba
    for i in range(3):
        usuario = User(
            username=f"User{i}",
            email=f"user{i}@teste.com",
            user_password="senha"
        )
        db.add(usuario)
        db.commit()
        usuario.genres.append(samba)
    
    db.commit()

    # Conta
    db.refresh(samba)
    quantidade = len(samba.users)

    assert quantidade == 3


def test_verificar_se_usuario_existe(db):
    """
    Teste básico: Verificar se um usuário existe pelo email.
    """
    # Cria usuário
    usuario = User(
        username="Teste",
        email="existe@teste.com",
        user_password="senha"
    )
    db.add(usuario)
    db.commit()

    # Verifica se existe
    existe = db.query(User).filter(User.email == "existe@teste.com").first() is not None
    nao_existe = db.query(User).filter(User.email == "naoexiste@teste.com").first() is not None

    assert existe is True
    assert nao_existe is False


# ============================================================================
# TESTES BÁSICOS DE ATUALIZAÇÃO EM LOTE
# ============================================================================


def test_atualizar_multiplos_artistas(db):
    """
    Teste básico: Atualizar múltiplos artistas de uma vez.
    """
    # Cria 3 artistas
    artistas = [
        Artist(artist_name=f"Banda {i}")
        for i in range(3)
    ]
    db.add_all(artistas)
    db.commit()

    # Atualiza todos adicionando " - Atualizado"
    for artista in artistas:
        artista.artist_name += " - Atualizado"
    
    db.commit()

    # Verifica
    for artista in artistas:
        db.refresh(artista)
        assert "Atualizado" in artista.artist_name


def test_deletar_multiplos_generos(db):
    """
    Teste básico: Deletar múltiplos gêneros.
    """
    # Cria 3 gêneros
    generos = [
        Genre(genre_name=f"Gênero {i}")
        for i in range(3)
    ]
    db.add_all(generos)
    db.commit()

    ids = [g.genre_id for g in generos]

    # Deleta todos
    for genero in generos:
        db.delete(genero)
    
    db.commit()

    # Verifica que foram deletados
    for genero_id in ids:
        assert db.get(Genre, genero_id) is None
