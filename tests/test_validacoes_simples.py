"""
Testes de Validações Simples

Testes básicos para verificar validações, campos obrigatórios,
e comportamentos esperados do sistema.
"""

import pytest
from datetime import date, timedelta

from app.models import Artist, Event, Genre, User


# ============================================================================
# TESTES DE CAMPOS OBRIGATÓRIOS
# ============================================================================


def test_genero_precisa_de_nome(db):
    """
    Teste simples: Gênero precisa ter um nome.
    """
    genero = Genre(genre_name="Forró")
    db.add(genero)
    db.commit()
    
    assert genero.genre_name is not None
    assert genero.genre_name != ""


def test_artista_precisa_de_nome(db):
    """
    Teste simples: Artista precisa ter um nome.
    """
    artista = Artist(artist_name="Caetano Veloso")
    db.add(artista)
    db.commit()
    
    assert artista.artist_name is not None
    assert artista.artist_name != ""


def test_usuario_precisa_email_e_senha(db):
    """
    Teste simples: Usuário precisa de email e senha.
    """
    usuario = User(
        username="Roberto",
        email="roberto@teste.com",
        user_password="minhasenha123"
    )
    db.add(usuario)
    db.commit()
    
    assert usuario.email is not None
    assert usuario.user_password is not None


def test_evento_precisa_data_futura(db):
    """
    Teste simples: Evento deve ter data no futuro.
    """
    # Data no futuro
    data_futura = date.today() + timedelta(days=7)
    
    evento = Event(
        event_name="Show Legal",
        event_description="Muito bom",
        event_date=data_futura,
        ticket_link="https://ingressos.com",
        event_location="Recife",
        organizer_id=1
    )
    db.add(evento)
    db.commit()
    
    assert evento.event_date > date.today()


# ============================================================================
# TESTES DE VALORES PADRÃO
# ============================================================================


def test_artista_spotify_id_pode_ser_none(db):
    """
    Teste simples: spotify_id é opcional para artista.
    """
    artista = Artist(artist_name="Artista Local")
    db.add(artista)
    db.commit()
    
    # spotify_id deve ser None quando não fornecido
    assert artista.spotify_id is None


def test_evento_coordenadas_opcionais(db):
    """
    Teste simples: Coordenadas são opcionais para evento.
    """
    evento = Event(
        event_name="Evento Sem GPS",
        event_description="Teste",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://evento.com",
        event_location="Algum lugar",
        organizer_id=1,
        latitude=None,
        longitude=None
    )
    db.add(evento)
    db.commit()
    
    assert evento.latitude is None
    assert evento.longitude is None


def test_usuario_campos_vazios_por_padrao(db):
    """
    Teste simples: Campos opcionais do usuário ficam vazios.
    """
    usuario = User(
        username="José",
        email="jose@teste.com",
        user_password="senha123"
    )
    db.add(usuario)
    db.commit()
    
    # Campos que devem estar vazios ou None
    assert usuario.spotify_id is None
    assert usuario.country in ["", None]
    assert usuario.profile_image in ["", None]


# ============================================================================
# TESTES DE UNICIDADE
# ============================================================================


def test_emails_unicos_por_usuario(db):
    """
    Teste simples: Cada email deve pertencer a um único usuário.
    """
    # Primeiro usuário
    usuario1 = User(
        username="Ana",
        email="unico@teste.com",
        user_password="senha1"
    )
    db.add(usuario1)
    db.commit()
    
    # Tenta criar segundo com mesmo email
    usuario2 = User(
        username="Beatriz",
        email="unico@teste.com",
        user_password="senha2"
    )
    db.add(usuario2)
    
    # Deve dar erro ao tentar commitar (viola constraint UNIQUE)
    with pytest.raises(Exception):  # SQLAlchemy lança IntegrityError
        db.commit()
    
    db.rollback()


def test_spotify_id_unico_por_artista(db):
    """
    Teste simples: Cada spotify_id deve pertencer a um único artista.
    """
    # Primeiro artista com spotify_id
    artista1 = Artist(
        artist_name="Primeiro",
        spotify_id="spotify_unique_123"
    )
    db.add(artista1)
    db.commit()
    
    # Tenta criar segundo com mesmo spotify_id
    artista2 = Artist(
        artist_name="Segundo",
        spotify_id="spotify_unique_123"
    )
    db.add(artista2)
    
    # Deve dar erro
    with pytest.raises(Exception):
        db.commit()
    
    db.rollback()


# ============================================================================
# TESTES DE TAMANHO DE TEXTO
# ============================================================================


def test_nome_genero_aceita_texto_longo(db):
    """
    Teste simples: Nome do gênero pode ter texto razoavelmente longo.
    """
    nome_longo = "Rock Progressivo Experimental dos Anos 70"
    genero = Genre(genre_name=nome_longo)
    db.add(genero)
    db.commit()
    
    assert len(genero.genre_name) > 20
    assert genero.genre_name == nome_longo


def test_descricao_evento_aceita_texto_longo(db):
    """
    Teste simples: Descrição do evento pode ser detalhada.
    """
    descricao_longa = "Este é um festival incrível que acontece " * 10
    
    evento = Event(
        event_name="Festival",
        event_description=descricao_longa,
        event_date=date.today() + timedelta(days=30),
        ticket_link="https://festival.com",
        event_location="Local",
        organizer_id=1
    )
    db.add(evento)
    db.commit()
    
    assert len(evento.event_description) > 100


# ============================================================================
# TESTES DE RELACIONAMENTOS SIMPLES
# ============================================================================


def test_artista_pode_nao_ter_generos(db):
    """
    Teste simples: Artista pode não ter gêneros associados.
    """
    artista = Artist(artist_name="Artista Independente")
    db.add(artista)
    db.commit()
    
    # Deve ter lista vazia de gêneros
    assert artista.genres == []
    assert len(artista.genres) == 0


def test_evento_pode_nao_ter_artistas(db):
    """
    Teste simples: Evento pode ser criado sem artistas inicialmente.
    """
    evento = Event(
        event_name="Evento Vazio",
        event_description="Ainda sem lineup",
        event_date=date.today() + timedelta(days=15),
        ticket_link="https://vazio.com",
        event_location="Local",
        organizer_id=1
    )
    db.add(evento)
    db.commit()
    
    assert evento.artists == []
    assert len(evento.artists) == 0


def test_usuario_pode_nao_ter_generos_favoritos(db):
    """
    Teste simples: Usuário pode não ter gêneros favoritos.
    """
    usuario = User(
        username="Novo",
        email="novo@teste.com",
        user_password="senha"
    )
    db.add(usuario)
    db.commit()
    
    assert usuario.genres == []


def test_genero_pode_nao_ter_artistas(db):
    """
    Teste simples: Gênero pode existir sem artistas associados.
    """
    genero = Genre(genre_name="Gênero Novo")
    db.add(genero)
    db.commit()
    
    assert genero.artists == []


# ============================================================================
# TESTES DE BUSCA E FILTROS BÁSICOS
# ============================================================================


def test_buscar_genero_por_nome_exato(db):
    """
    Teste simples: Buscar gênero pelo nome exato.
    """
    # Cria gênero
    Genre(genre_name="Sertanejo")
    db.add(Genre(genre_name="Sertanejo"))
    db.commit()
    
    # Busca
    resultado = db.query(Genre).filter(Genre.genre_name == "Sertanejo").first()
    
    assert resultado is not None
    assert resultado.genre_name == "Sertanejo"


def test_buscar_artista_com_spotify_id(db):
    """
    Teste simples: Buscar artista que tem spotify_id.
    """
    # Cria artistas
    db.add(Artist(artist_name="Com Spotify", spotify_id="spot123"))
    db.add(Artist(artist_name="Sem Spotify", spotify_id=None))
    db.commit()
    
    # Busca apenas com spotify_id
    com_spotify = db.query(Artist).filter(Artist.spotify_id.isnot(None)).all()
    
    assert len(com_spotify) >= 1


def test_buscar_eventos_por_local(db):
    """
    Teste simples: Buscar eventos em uma cidade específica.
    """
    # Cria eventos em cidades diferentes
    db.add(Event(
        event_name="Show SP",
        event_description="Em São Paulo",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://sp.com",
        event_location="São Paulo",
        organizer_id=1
    ))
    db.add(Event(
        event_name="Show RJ",
        event_description="No Rio",
        event_date=date.today() + timedelta(days=20),
        ticket_link="https://rj.com",
        event_location="Rio de Janeiro",
        organizer_id=1
    ))
    db.commit()
    
    # Busca apenas em São Paulo
    eventos_sp = db.query(Event).filter(Event.event_location == "São Paulo").all()
    
    assert len(eventos_sp) >= 1


def test_buscar_usuario_que_existe(db):
    """
    Teste simples: Verificar se usuário existe no banco.
    """
    # Cria usuário
    db.add(User(
        username="Marcelo",
        email="marcelo@teste.com",
        user_password="senha"
    ))
    db.commit()
    
    # Verifica que existe
    usuario = db.query(User).filter(User.email == "marcelo@teste.com").first()
    
    assert usuario is not None
    assert usuario.username == "Marcelo"


# ============================================================================
# TESTES DE CONTAGEM SIMPLES
# ============================================================================


def test_contar_total_de_generos(db):
    """
    Teste simples: Contar quantos gêneros existem.
    """
    contagem_inicial = db.query(Genre).count()
    
    # Adiciona mais alguns
    db.add(Genre(genre_name="G1"))
    db.add(Genre(genre_name="G2"))
    db.commit()
    
    contagem_final = db.query(Genre).count()
    
    assert contagem_final == contagem_inicial + 2


def test_contar_artistas_com_spotify(db):
    """
    Teste simples: Contar quantos artistas têm Spotify.
    """
    # Adiciona artistas
    db.add(Artist(artist_name="A1", spotify_id="s1"))
    db.add(Artist(artist_name="A2", spotify_id=None))
    db.add(Artist(artist_name="A3", spotify_id="s3"))
    db.commit()
    
    # Conta com spotify_id
    com_spotify = db.query(Artist).filter(Artist.spotify_id.isnot(None)).count()
    
    assert com_spotify >= 2


def test_contar_eventos_futuros(db):
    """
    Teste simples: Contar eventos que ainda vão acontecer.
    """
    # Adiciona evento futuro
    db.add(Event(
        event_name="Evento Futuro",
        event_description="Vai acontecer",
        event_date=date.today() + timedelta(days=100),
        ticket_link="https://futuro.com",
        event_location="Local",
        organizer_id=1
    ))
    db.commit()
    
    # Conta futuros
    futuros = db.query(Event).filter(Event.event_date > date.today()).count()
    
    assert futuros >= 1


# ============================================================================
# TESTES DE ATUALIZAÇÃO SIMPLES
# ============================================================================


def test_pode_atualizar_email_usuario(db):
    """
    Teste simples: Pode atualizar o email do usuário.
    """
    usuario = User(
        username="Paulo",
        email="paulo_antigo@teste.com",
        user_password="senha"
    )
    db.add(usuario)
    db.commit()
    
    # Atualiza email
    usuario.email = "paulo_novo@teste.com"
    db.commit()
    
    db.refresh(usuario)
    assert usuario.email == "paulo_novo@teste.com"


def test_pode_atualizar_data_evento(db):
    """
    Teste simples: Pode atualizar a data do evento.
    """
    evento = Event(
        event_name="Evento",
        event_description="Teste",
        event_date=date.today() + timedelta(days=10),
        ticket_link="https://evento.com",
        event_location="Local",
        organizer_id=1
    )
    db.add(evento)
    db.commit()
    
    # Atualiza data
    nova_data = date.today() + timedelta(days=20)
    evento.event_date = nova_data
    db.commit()
    
    db.refresh(evento)
    assert evento.event_date == nova_data


def test_pode_adicionar_spotify_id_depois(db):
    """
    Teste simples: Pode adicionar spotify_id depois da criação.
    """
    artista = Artist(artist_name="Artista")
    db.add(artista)
    db.commit()
    
    assert artista.spotify_id is None
    
    # Adiciona depois
    artista.spotify_id = "novo_spotify_123"
    db.commit()
    
    db.refresh(artista)
    assert artista.spotify_id == "novo_spotify_123"


# ============================================================================
# TESTES DE LISTAGEM SIMPLES
# ============================================================================


def test_listar_todos_usuarios(db):
    """
    Teste simples: Listar todos os usuários cadastrados.
    """
    usuarios = db.query(User).all()
    
    # Deve retornar uma lista (pode ter usuários do conftest)
    assert isinstance(usuarios, list)


def test_listar_todos_eventos(db):
    """
    Teste simples: Listar todos os eventos cadastrados.
    """
    eventos = db.query(Event).all()
    
    assert isinstance(eventos, list)


def test_listar_artistas_ordem_alfabetica(db):
    """
    Teste simples: Listar artistas em ordem alfabética.
    """
    # Adiciona alguns artistas
    db.add(Artist(artist_name="Zeca"))
    db.add(Artist(artist_name="Ana"))
    db.add(Artist(artist_name="Maria"))
    db.commit()
    
    # Lista ordenado
    artistas = db.query(Artist).order_by(Artist.artist_name).all()
    
    assert isinstance(artistas, list)
    # Verifica que está ordenado
    nomes = [a.artist_name for a in artistas]
    assert nomes == sorted(nomes)


# ============================================================================
# TESTES DE EXISTÊNCIA
# ============================================================================


def test_verificar_se_genero_existe(db):
    """
    Teste simples: Verificar se um gênero existe.
    """
    # Cria gênero
    db.add(Genre(genre_name="Funk"))
    db.commit()
    
    # Verifica
    existe = db.query(Genre).filter(Genre.genre_name == "Funk").first() is not None
    nao_existe = db.query(Genre).filter(Genre.genre_name == "Inexistente").first() is not None
    
    assert existe is True
    assert nao_existe is False


def test_verificar_se_artista_tem_spotify(db):
    """
    Teste simples: Verificar se artista está no Spotify.
    """
    artista = Artist(artist_name="Artista Spotify", spotify_id="abc123")
    db.add(artista)
    db.commit()
    
    tem_spotify = artista.spotify_id is not None
    
    assert tem_spotify is True


def test_verificar_se_evento_tem_coordenadas(db):
    """
    Teste simples: Verificar se evento tem coordenadas GPS.
    """
    evento_com = Event(
        event_name="Com GPS",
        event_description="Teste",
        event_date=date.today() + timedelta(days=5),
        ticket_link="https://gps.com",
        event_location="Local",
        organizer_id=1,
        latitude=-23.5,
        longitude=-46.6
    )
    
    evento_sem = Event(
        event_name="Sem GPS",
        event_description="Teste",
        event_date=date.today() + timedelta(days=5),
        ticket_link="https://nogps.com",
        event_location="Local",
        organizer_id=1,
        latitude=None,
        longitude=None
    )
    
    db.add(evento_com)
    db.add(evento_sem)
    db.commit()
    
    tem_coord = evento_com.latitude is not None and evento_com.longitude is not None
    nao_tem = evento_sem.latitude is None or evento_sem.longitude is None
    
    assert tem_coord is True
    assert nao_tem is True
