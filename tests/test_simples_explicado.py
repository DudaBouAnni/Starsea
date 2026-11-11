"""
Testes Simples e Explicados 🎓

Este arquivo contém testes SUPER simples das funções,
com comentários linha por linha explicando o que está acontecendo.

Perfeito para quem está começando!
"""

from datetime import date, timedelta
from app.models import Artist, Event, Genre, User
from app.services.geo_service import distance_km, has_coordinates, local_today


# ===========================================================================
# TESTANDO FUNÇÕES DE DATA
# ===========================================================================


def test_local_today_explicado(db):
    """
    Testa a função local_today() que retorna a data de hoje.
    
    O que ela faz: Retorna a data atual no fuso horário de São Paulo.
    """
    # Chama a função que queremos testar
    hoje = local_today()
    
    # Verifica se retornou um objeto de data (não None, não string, etc)
    assert hoje is not None  # ✅ Não pode ser None
    
    # Verifica se é realmente uma data
    assert isinstance(hoje, date)  # ✅ Tem que ser tipo 'date'
    
    # Pronto! Se chegou aqui, a função está funcionando ✨


# ===========================================================================
# TESTANDO FUNÇÕES DE COORDENADAS
# ===========================================================================


def test_has_coordinates_com_coordenadas_validas(db):
    """
    Testa se a função has_coordinates() detecta quando tem coordenadas.
    
    O que ela faz: Verifica se um objeto tem latitude E longitude.
    """
    # Cria um evento COM coordenadas
    evento = Event(
        event_name="Show com GPS",
        event_description="Tem localização",
        event_date=date.today() + timedelta(days=5),
        ticket_link="https://show.com",
        event_location="São Paulo",
        organizer_id=1,
        latitude=-23.5505,    # ← Tem latitude
        longitude=-46.6333    # ← Tem longitude
    )
    
    # Testa se a função detecta que tem coordenadas
    resultado = has_coordinates(evento)
    
    # Deve retornar True porque o evento TEM latitude e longitude
    assert resultado is True  # ✅ Tem coordenadas!


def test_has_coordinates_sem_coordenadas(db):
    """
    Testa se a função has_coordinates() detecta quando NÃO tem coordenadas.
    
    Caso contrário: quando faltam as coordenadas.
    """
    # Cria um evento SEM coordenadas (None)
    evento = Event(
        event_name="Show sem GPS",
        event_description="Sem localização",
        event_date=date.today() + timedelta(days=5),
        ticket_link="https://show.com",
        event_location="Algum lugar",
        organizer_id=1,
        latitude=None,     # ← SEM latitude
        longitude=None     # ← SEM longitude
    )
    
    # Testa se a função detecta que NÃO tem coordenadas
    resultado = has_coordinates(evento)
    
    # Deve retornar False porque faltam as coordenadas
    assert resultado is False  # ✅ Não tem coordenadas!


# ===========================================================================
# TESTANDO FUNÇÕES DE DISTÂNCIA
# ===========================================================================


def test_distance_km_mesmo_ponto(db):
    """
    Testa se a distância entre o mesmo ponto é zero.
    
    O que ela faz: Calcula distância em km entre duas coordenadas.
    Caso especial: do mesmo ponto para ele mesmo = 0 km
    """
    # Coordenadas de São Paulo
    lat = -23.5505
    lon = -46.6333
    
    # Calcula a distância de São Paulo para São Paulo (mesmo ponto)
    distancia = distance_km(lat, lon, lat, lon)
    
    # A distância de um ponto para ele mesmo é ZERO
    assert distancia == 0.0  # ✅ Zero km!


def test_distance_km_pontos_diferentes(db):
    """
    Testa se calcula distância correta entre dois pontos diferentes.
    
    Exemplo real: São Paulo até Rio de Janeiro
    """
    # Coordenadas de São Paulo
    sp_lat = -23.5505
    sp_lon = -46.6333
    
    # Coordenadas do Rio de Janeiro
    rj_lat = -22.9068
    rj_lon = -43.1729
    
    # Calcula a distância entre SP e RJ
    distancia = distance_km(sp_lat, sp_lon, rj_lat, rj_lon)
    
    # A distância real é aproximadamente 360 km
    # Verificamos se está nessa faixa (entre 350 e 370)
    assert 350 < distancia < 370  # ✅ Aproximadamente 360 km!
    
    # Também verificamos que não é zero (são pontos diferentes!)
    assert distancia > 0  # ✅ Distância maior que zero!


def test_distance_km_simetrico(db):
    """
    Testa se a distância é igual em ambas direções.
    
    Lógica: A → B deve ser igual a B → A
    """
    # Dois pontos quaisquer
    ponto1_lat = -23.5
    ponto1_lon = -46.6
    ponto2_lat = -22.9
    ponto2_lon = -43.1
    
    # Calcula distância do ponto 1 para o ponto 2
    distancia_1_para_2 = distance_km(ponto1_lat, ponto1_lon, ponto2_lat, ponto2_lon)
    
    # Calcula distância do ponto 2 para o ponto 1 (invertido!)
    distancia_2_para_1 = distance_km(ponto2_lat, ponto2_lon, ponto1_lat, ponto1_lon)
    
    # As duas distâncias devem ser IGUAIS (não importa a direção)
    assert distancia_1_para_2 == distancia_2_para_1  # ✅ A→B = B→A


# ===========================================================================
# TESTANDO CRIAÇÃO DE OBJETOS SIMPLES
# ===========================================================================


def test_criar_genero_simples(db):
    """
    Testa criar um gênero musical.
    
    Objetivo: Verificar que conseguimos criar e salvar um gênero.
    """
    # 1️⃣ Cria um objeto Genre (gênero musical)
    genero = Genre(genre_name="Rock")
    
    # 2️⃣ Adiciona ao banco de dados (prepara para salvar)
    db.add(genero)
    
    # 3️⃣ Salva no banco (commit = confirmar)
    db.commit()
    
    # 4️⃣ Verifica se foi criado com sucesso
    assert genero.genre_id is not None  # ✅ Tem ID = foi salvo!
    assert genero.genre_name == "Rock"  # ✅ Nome está correto!


def test_criar_artista_simples(db):
    """
    Testa criar um artista.
    
    Passos: criar → salvar → verificar
    """
    # Cria um artista
    artista = Artist(artist_name="Beatles")
    
    # Salva no banco
    db.add(artista)
    db.commit()
    
    # Verifica
    assert artista.artist_id is not None  # ✅ Foi salvo (tem ID)
    assert artista.artist_name == "Beatles"  # ✅ Nome certo


def test_criar_usuario_simples(db):
    """
    Testa criar um usuário.
    
    Um usuário precisa de: nome, email e senha
    """
    # Cria usuário com os dados mínimos necessários
    usuario = User(
        username="Maria",           # Nome do usuário
        email="maria@teste.com",    # Email (tem que ser único!)
        user_password="senha123"    # Senha
    )
    
    # Salva
    db.add(usuario)
    db.commit()
    
    # Verifica que foi criado
    assert usuario.user_id is not None      # ✅ Tem ID
    assert usuario.username == "Maria"      # ✅ Nome OK
    assert usuario.email == "maria@teste.com"  # ✅ Email OK


# ===========================================================================
# TESTANDO BUSCA DE OBJETOS
# ===========================================================================


def test_buscar_genero_por_id(db):
    """
    Testa buscar um gênero pelo ID.
    
    Fluxo: criar → salvar → buscar → verificar
    """
    # 1️⃣ Primeiro, cria e salva um gênero
    genero = Genre(genre_name="Jazz")
    db.add(genero)
    db.commit()
    
    # Guarda o ID que foi gerado
    id_salvo = genero.genre_id
    
    # 2️⃣ Agora busca esse gênero pelo ID
    genero_encontrado = db.get(Genre, id_salvo)
    
    # 3️⃣ Verifica que encontrou
    assert genero_encontrado is not None  # ✅ Encontrou!
    assert genero_encontrado.genre_name == "Jazz"  # ✅ É o correto!
    assert genero_encontrado.genre_id == id_salvo  # ✅ ID bate!


def test_buscar_artista_por_nome(db):
    """
    Testa buscar um artista pelo nome.
    
    Diferente de buscar por ID, aqui buscamos por um campo qualquer.
    """
    # Cria e salva um artista
    artista = Artist(artist_name="Queen")
    db.add(artista)
    db.commit()
    
    # Busca pelo nome usando query + filter
    encontrado = db.query(Artist).filter(
        Artist.artist_name == "Queen"  # ← Condição: nome = "Queen"
    ).first()  # .first() = pega o primeiro resultado
    
    # Verifica
    assert encontrado is not None  # ✅ Achou!
    assert encontrado.artist_name == "Queen"  # ✅ Nome certo!


# ===========================================================================
# TESTANDO ATUALIZAÇÃO DE OBJETOS
# ===========================================================================


def test_atualizar_nome_genero(db):
    """
    Testa atualizar (modificar) dados de um gênero.
    
    Fluxo: criar → salvar → modificar → salvar → verificar
    """
    # 1️⃣ Cria com um nome
    genero = Genre(genre_name="Rap")
    db.add(genero)
    db.commit()
    
    # 2️⃣ Modifica o nome
    genero.genre_name = "Hip Hop"  # ← Mudou!
    
    # 3️⃣ Salva a modificação
    db.commit()
    
    # 4️⃣ Recarrega do banco para ter certeza
    db.refresh(genero)
    
    # 5️⃣ Verifica que mudou
    assert genero.genre_name == "Hip Hop"  # ✅ Nome atualizado!


def test_atualizar_artista(db):
    """
    Testa atualizar nome de um artista.
    """
    # Cria
    artista = Artist(artist_name="Nome Antigo")
    db.add(artista)
    db.commit()
    
    # Atualiza
    artista.artist_name = "Nome Novo"
    db.commit()
    
    # Recarrega e verifica
    db.refresh(artista)
    assert artista.artist_name == "Nome Novo"  # ✅ Mudou!


# ===========================================================================
# TESTANDO EXCLUSÃO DE OBJETOS
# ===========================================================================


def test_deletar_genero(db):
    """
    Testa deletar (remover) um gênero.
    
    Fluxo: criar → salvar → deletar → verificar que sumiu
    """
    # 1️⃣ Cria e salva
    genero = Genre(genre_name="Temporário")
    db.add(genero)
    db.commit()
    
    # Guarda o ID
    id_do_genero = genero.genre_id
    
    # 2️⃣ Deleta
    db.delete(genero)
    db.commit()
    
    # 3️⃣ Tenta buscar de novo (não deve achar)
    genero_deletado = db.get(Genre, id_do_genero)
    
    # Verifica que não existe mais
    assert genero_deletado is None  # ✅ Foi deletado! (None = não achou)


def test_deletar_artista(db):
    """
    Testa deletar um artista.
    """
    # Cria
    artista = Artist(artist_name="Artista Temporário")
    db.add(artista)
    db.commit()
    id_artista = artista.artist_id
    
    # Deleta
    db.delete(artista)
    db.commit()
    
    # Verifica que sumiu
    assert db.get(Artist, id_artista) is None  # ✅ Deletado!


# ===========================================================================
# TESTANDO RELACIONAMENTOS SIMPLES
# ===========================================================================


def test_adicionar_genero_ao_artista_explicado(db):
    """
    Testa associar um gênero a um artista.
    
    Explicação: Um artista pode ter vários gêneros.
    Por exemplo: "Artista X faz Rock e Blues"
    """
    # 1️⃣ Cria um gênero
    rock = Genre(genre_name="Rock")
    db.add(rock)
    db.commit()
    
    # 2️⃣ Cria um artista
    artista = Artist(artist_name="AC/DC")
    db.add(artista)
    db.commit()
    
    # 3️⃣ Associa o gênero ao artista
    artista.genres.append(rock)  # ← "AC/DC faz Rock"
    db.commit()
    
    # 4️⃣ Recarrega o artista
    db.refresh(artista)
    
    # 5️⃣ Verifica que o gênero está lá
    assert len(artista.genres) == 1  # ✅ Tem 1 gênero
    assert rock in artista.genres    # ✅ É o gênero Rock!


def test_adicionar_multiplos_generos(db):
    """
    Testa adicionar vários gêneros ao mesmo artista.
    
    Exemplo: "David Bowie faz Rock, Pop e Glam"
    """
    # Cria 3 gêneros
    rock = Genre(genre_name="Rock")
    pop = Genre(genre_name="Pop")
    glam = Genre(genre_name="Glam")
    
    db.add_all([rock, pop, glam])  # Adiciona todos de uma vez
    db.commit()
    
    # Cria artista
    artista = Artist(artist_name="David Bowie")
    db.add(artista)
    db.commit()
    
    # Adiciona os 3 gêneros ao artista
    artista.genres.append(rock)
    artista.genres.append(pop)
    artista.genres.append(glam)
    db.commit()
    
    # Verifica
    db.refresh(artista)
    assert len(artista.genres) == 3  # ✅ Tem 3 gêneros!


# ===========================================================================
# TESTANDO CONTAGENS
# ===========================================================================


def test_contar_generos(db):
    """
    Testa contar quantos gêneros existem no banco.
    
    Função: .count() retorna a quantidade
    """
    # Conta quantos gêneros existem agora
    contagem_inicial = db.query(Genre).count()
    
    # Adiciona 3 novos gêneros
    db.add(Genre(genre_name="G1"))
    db.add(Genre(genre_name="G2"))
    db.add(Genre(genre_name="G3"))
    db.commit()
    
    # Conta de novo
    contagem_final = db.query(Genre).count()
    
    # Deve ter aumentado em 3
    assert contagem_final == contagem_inicial + 3  # ✅ +3 gêneros!


def test_contar_artistas(db):
    """
    Testa contar artistas.
    """
    # Conta inicial
    antes = db.query(Artist).count()
    
    # Adiciona 2 artistas
    db.add(Artist(artist_name="A1"))
    db.add(Artist(artist_name="A2"))
    db.commit()
    
    # Conta depois
    depois = db.query(Artist).count()
    
    # Verificação
    assert depois == antes + 2  # ✅ +2 artistas!


# ===========================================================================
# TESTANDO VERIFICAÇÕES SIMPLES
# ===========================================================================


def test_verificar_se_genero_existe(db):
    """
    Testa verificar se um gênero existe no banco.
    
    Retorna True se existe, False se não existe.
    """
    # Cria um gênero
    db.add(Genre(genre_name="Samba"))
    db.commit()
    
    # Verifica se "Samba" existe
    existe_samba = db.query(Genre).filter(
        Genre.genre_name == "Samba"
    ).first() is not None  # ← is not None = existe!
    
    # Verifica se "Inexistente" existe
    existe_fake = db.query(Genre).filter(
        Genre.genre_name == "Inexistente"
    ).first() is not None
    
    # Testes
    assert existe_samba is True   # ✅ Samba existe!
    assert existe_fake is False   # ✅ Inexistente não existe!


def test_verificar_campo_none(db):
    """
    Testa verificar se um campo é None (vazio).
    
    Exemplo: spotify_id pode ser None quando o artista é local.
    """
    # Cria artista SEM spotify_id
    artista = Artist(artist_name="Artista Local")
    db.add(artista)
    db.commit()
    
    # Verifica que spotify_id é None
    assert artista.spotify_id is None  # ✅ Não tem Spotify!


def test_verificar_campo_preenchido(db):
    """
    Testa verificar se um campo foi preenchido.
    """
    # Cria artista COM spotify_id
    artista = Artist(
        artist_name="Artista Spotify",
        spotify_id="abc123"  # ← Preenchido!
    )
    db.add(artista)
    db.commit()
    
    # Verifica que está preenchido (não é None)
    assert artista.spotify_id is not None  # ✅ Tem Spotify!
    assert artista.spotify_id == "abc123"  # ✅ Valor correto!


# ===========================================================================
# RESUMO DO QUE APRENDEMOS 🎓
# ===========================================================================

"""
✅ Testar funções simples:
   - Chamar a função
   - Verificar o resultado com assert

✅ Testar CRUD:
   - Create: criar → salvar → verificar ID
   - Read: criar → buscar → comparar
   - Update: criar → modificar → verificar mudança
   - Delete: criar → deletar → verificar que sumiu

✅ Testar relacionamentos:
   - Criar objetos
   - Associar com .append()
   - Verificar com 'in' ou len()

✅ Comandos importantes:
   - db.add() = prepara para salvar
   - db.commit() = salva de verdade
   - db.refresh() = recarrega do banco
   - db.get(Model, id) = busca por ID
   - db.query(Model) = faz consultas
   - .filter() = filtra resultados
   - .first() = pega primeiro
   - .all() = pega todos
   - .count() = conta quantos

✅ Asserts comuns:
   - assert x is not None  (não é vazio)
   - assert x == y  (são iguais)
   - assert x in lista  (está na lista)
   - assert len(lista) == 5  (tamanho certo)

🎉 Agora você sabe testar funções básicas!
"""
