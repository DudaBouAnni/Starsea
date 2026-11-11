"""
Testes unitários para o serviço de geolocalização (geo_service.py)

Este módulo testa as funções utilitárias para cálculos geográficos
e manipulação de datas baseadas em fuso horário.
"""

from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest

from app.models import Event
from app.services.geo_service import distance_km, has_coordinates, local_today


# ============================================================================
# TESTES DE DATA LOCAL (local_today)
# ============================================================================


def test_local_today_returns_date_object():
    """
    Testa que a função local_today retorna um objeto de data.
    
    Verifica que:
    - O retorno é do tipo date
    - Não retorna datetime (apenas a data sem hora)
    """
    result = local_today()

    assert isinstance(result, date)
    assert not isinstance(result, datetime)


def test_local_today_uses_sao_paulo_timezone():
    """
    Testa que local_today usa o fuso horário de São Paulo.
    
    Verifica que:
    - A data retornada corresponde ao horário de São Paulo
    - Independente do fuso horário do sistema
    
    Nota: Este teste assume que a data será sempre válida
    no fuso horário de São Paulo.
    """
    result = local_today()

    # Obtém a data atual em São Paulo para comparação
    sao_paulo_now = datetime.now(ZoneInfo("America/Sao_Paulo")).date()

    assert result == sao_paulo_now


def test_local_today_is_consistent_across_calls():
    """
    Testa que chamadas sucessivas retornam a mesma data
    (quando feitas no mesmo dia).
    
    Verifica que:
    - A função é consistente
    - Não há variação aleatória
    """
    date1 = local_today()
    date2 = local_today()

    # As duas chamadas devem retornar a mesma data
    assert date1 == date2


# ============================================================================
# TESTES DE VERIFICAÇÃO DE COORDENADAS (has_coordinates)
# ============================================================================


def test_has_coordinates_with_valid_coordinates():
    """
    Testa a verificação de coordenadas válidas em uma entidade.
    
    Verifica que:
    - Retorna True quando latitude e longitude estão presentes
    - Aceita qualquer valor numérico (incluindo zero e negativos)
    """

    class MockEntity:
        def __init__(self, lat, lon):
            self.latitude = lat
            self.longitude = lon

    # Coordenadas válidas normais
    entity1 = MockEntity(-23.5505, -46.6333)
    assert has_coordinates(entity1) is True

    # Coordenadas no equador/meridiano principal
    entity2 = MockEntity(0, 0)
    assert has_coordinates(entity2) is True

    # Coordenadas extremas
    entity3 = MockEntity(90, 180)
    assert has_coordinates(entity3) is True

    entity4 = MockEntity(-90, -180)
    assert has_coordinates(entity4) is True


def test_has_coordinates_with_missing_latitude():
    """
    Testa quando a latitude está ausente (None).
    
    Verifica que:
    - Retorna False quando latitude é None
    - Mesmo que longitude esteja presente
    """

    class MockEntity:
        def __init__(self, lat, lon):
            self.latitude = lat
            self.longitude = lon

    entity = MockEntity(None, -46.6333)
    assert has_coordinates(entity) is False


def test_has_coordinates_with_missing_longitude():
    """
    Testa quando a longitude está ausente (None).
    
    Verifica que:
    - Retorna False quando longitude é None
    - Mesmo que latitude esteja presente
    """

    class MockEntity:
        def __init__(self, lat, lon):
            self.latitude = lat
            self.longitude = lon

    entity = MockEntity(-23.5505, None)
    assert has_coordinates(entity) is False


def test_has_coordinates_with_both_missing():
    """
    Testa quando ambas as coordenadas estão ausentes.
    
    Verifica que:
    - Retorna False quando latitude e longitude são None
    """

    class MockEntity:
        def __init__(self, lat, lon):
            self.latitude = lat
            self.longitude = lon

    entity = MockEntity(None, None)
    assert has_coordinates(entity) is False


def test_has_coordinates_with_zero_values():
    """
    Testa que valores zero são considerados coordenadas válidas.
    
    Verifica que:
    - Zero é diferente de None
    - Coordenadas (0, 0) são válidas (Golfo da Guiné)
    """

    class MockEntity:
        def __init__(self, lat, lon):
            self.latitude = lat
            self.longitude = lon

    entity = MockEntity(0.0, 0.0)
    assert has_coordinates(entity) is True


# ============================================================================
# TESTES DE CÁLCULO DE DISTÂNCIA (distance_km)
# ============================================================================


def test_distance_km_same_point_returns_zero():
    """
    Testa o cálculo de distância entre o mesmo ponto.
    
    Verifica que:
    - A distância de um ponto para ele mesmo é zero
    - Funciona com coordenadas variadas
    """
    # São Paulo para São Paulo
    distance = distance_km(-23.5505, -46.6333, -23.5505, -46.6333)
    assert distance == 0.0

    # Equador para Equador
    distance = distance_km(0, 0, 0, 0)
    assert distance == 0.0

    # Polo Norte para Polo Norte
    distance = distance_km(90, 0, 90, 0)
    assert distance == 0.0


def test_distance_km_calculates_correctly():
    """
    Testa o cálculo de distância entre pontos conhecidos.
    
    Verifica que:
    - A distância é calculada usando a fórmula de Haversine
    - Os valores estão dentro da margem de erro esperada
    
    Exemplos:
    - São Paulo a Rio de Janeiro: ~360 km
    - Equador: 1 grau de longitude ≈ 111.195 km
    """
    # São Paulo (-23.5505, -46.6333) para Rio de Janeiro (-22.9068, -43.1729)
    # Distância aproximada: 360 km
    distance_sp_rj = distance_km(-23.5505, -46.6333, -22.9068, -43.1729)
    assert 350 < distance_sp_rj < 370

    # No equador, 1 grau de longitude é aproximadamente 111.195 km
    distance_equator = distance_km(0, 0, 0, 1)
    assert pytest.approx(distance_equator, abs=0.01) == 111.195


def test_distance_km_across_hemispheres():
    """
    Testa o cálculo de distância entre hemisférios diferentes.
    
    Verifica que:
    - A função lida corretamente com coordenadas em hemisférios opostos
    - Valores negativos são tratados adequadamente
    """
    # Do hemisfério norte ao sul
    distance = distance_km(45, 0, -45, 0)
    # 90 graus de latitude = 90 * 111.195 km ≈ 10007.5 km
    assert 9900 < distance < 10100


def test_distance_km_across_antimeridian():
    """
    Testa o cálculo de distância cruzando o antimeridiano (linha de data).
    
    Verifica que:
    - A função calcula corretamente mesmo cruzando longitude 180/-180
    """
    # De 170° para -170° no equador (20° de diferença)
    distance = distance_km(0, 170, 0, -170)
    # 20 graus no equador ≈ 20 * 111.195 km ≈ 2224 km
    assert 2200 < distance < 2250


def test_distance_km_maximum_distance():
    """
    Testa o cálculo da máxima distância possível na Terra.
    
    Verifica que:
    - Pontos antípodas (opostos) geram a maior distância
    - A distância é aproximadamente metade da circunferência da Terra
    
    Nota: A circunferência da Terra é ~40075 km, então a
    distância máxima é ~20037 km.
    """
    # Pontos antípodas: (0, 0) e (0, 180)
    distance = distance_km(0, 0, 0, 180)
    # Aproximadamente metade da circunferência equatorial
    assert pytest.approx(distance, abs=1) == 20015.114


def test_distance_km_with_negative_coordinates():
    """
    Testa o cálculo com coordenadas negativas (hemisfério sul/oeste).
    
    Verifica que:
    - Coordenadas negativas são tratadas corretamente
    - O cálculo funciona para qualquer combinação de sinais
    """
    # Buenos Aires (-34.6037, -58.3816) para Sydney (-33.8688, 151.2093)
    # Distância muito grande (atravessando o Pacífico)
    distance = distance_km(-34.6037, -58.3816, -33.8688, 151.2093)
    # Aproximadamente 11,800 km
    assert 11700 < distance < 11900


def test_distance_km_precision_with_close_points():
    """
    Testa a precisão do cálculo com pontos muito próximos.
    
    Verifica que:
    - A função mantém precisão mesmo com diferenças pequenas
    - Não há problemas de arredondamento significativos
    """
    # Dois pontos separados por 0.001 graus (~111 metros)
    distance = distance_km(-23.5505, -46.6333, -23.5515, -46.6333)
    # Aproximadamente 0.111 km
    assert 0.10 < distance < 0.12


def test_distance_km_at_poles():
    """
    Testa o cálculo de distância em latitudes extremas (polos).
    
    Verifica que:
    - A função funciona corretamente próximo aos polos
    - Não há divisões por zero ou erros matemáticos
    """
    # Do polo norte (90, 0) para um ponto próximo (89, 0)
    distance = distance_km(90, 0, 89, 0)
    # 1 grau de latitude ≈ 111.195 km
    assert 110 < distance < 112

    # Polo sul
    distance = distance_km(-90, 0, -89, 0)
    assert 110 < distance < 112


def test_distance_km_formula_haversine():
    """
    Testa que a fórmula implementada é realmente a de Haversine.
    
    Verifica que:
    - Os resultados correspondem à fórmula de Haversine
    - O raio da Terra usado é apropriado (6371.0088 km)
    
    A fórmula de Haversine calcula a distância sobre a esfera,
    não a distância por vias terrestres.
    """
    # Pontos de teste conhecidos
    lat1, lon1 = 52.5200, 13.4050  # Berlim
    lat2, lon2 = 41.9028, 12.4964  # Roma

    distance = distance_km(lat1, lon1, lat2, lon2)

    # Distância conhecida: aproximadamente 1182 km
    assert 1170 < distance < 1195


def test_distance_km_symmetry():
    """
    Testa a simetria do cálculo de distância.
    
    Verifica que:
    - distance(A, B) == distance(B, A)
    - A ordem dos pontos não importa
    """
    lat1, lon1 = -23.5505, -46.6333  # São Paulo
    lat2, lon2 = -22.9068, -43.1729  # Rio de Janeiro

    distance_ab = distance_km(lat1, lon1, lat2, lon2)
    distance_ba = distance_km(lat2, lon2, lat1, lon1)

    assert distance_ab == distance_ba


# ============================================================================
# TESTES DE INTEGRAÇÃO COM MODELOS
# ============================================================================


def test_has_coordinates_with_event_model(db):
    """
    Testa has_coordinates com o modelo Event real.
    
    Verifica que:
    - A função funciona com modelos do banco de dados
    - Integra corretamente com a estrutura do projeto
    """
    from datetime import timedelta

    # Evento com coordenadas
    event_with_coords = Event(
        event_name="Show com Localização",
        event_description="Teste",
        event_date=local_today() + timedelta(days=1),
        ticket_link="https://example.com",
        event_location="São Paulo",
        organizer_id=1,
        latitude=-23.5505,
        longitude=-46.6333,
    )

    assert has_coordinates(event_with_coords) is True

    # Evento sem coordenadas
    event_without_coords = Event(
        event_name="Show sem Localização",
        event_description="Teste",
        event_date=local_today() + timedelta(days=1),
        ticket_link="https://example.com",
        event_location="Local Desconhecido",
        organizer_id=1,
        latitude=None,
        longitude=None,
    )

    assert has_coordinates(event_without_coords) is False


# ============================================================================
# TESTES DE CASOS EXTREMOS (EDGE CASES)
# ============================================================================


def test_distance_km_handles_floating_point_precision():
    """
    Testa que a função lida corretamente com precisão de ponto flutuante.
    
    Verifica que:
    - Não há overflow ou underflow
    - Resultados são estáveis e reproduzíveis
    """
    # Coordenadas com muitas casas decimais
    distance = distance_km(
        -23.550520183, -46.633308471, -23.550520184, -46.633308472
    )

    # Distância extremamente pequena, mas não zero
    assert distance >= 0
    assert distance < 0.001  # Menos de 1 metro


def test_distance_km_boundary_latitudes():
    """
    Testa o cálculo nos limites de latitude (-90 a 90).
    
    Verifica que:
    - A função aceita todos os valores válidos de latitude
    - Não há erros nos extremos
    """
    # Latitude máxima (polo norte)
    distance_max = distance_km(90, 0, 89, 0)
    assert distance_max > 0

    # Latitude mínima (polo sul)
    distance_min = distance_km(-90, 0, -89, 0)
    assert distance_min > 0

    # Entre os polos
    distance_poles = distance_km(90, 0, -90, 0)
    # Aproximadamente metade da circunferência meridional
    assert 19900 < distance_poles < 20100


def test_distance_km_boundary_longitudes():
    """
    Testa o cálculo nos limites de longitude (-180 a 180).
    
    Verifica que:
    - A função aceita todos os valores válidos de longitude
    - Trata corretamente o "wrap around" em ±180°
    """
    # No equador, de -180 a -179
    distance = distance_km(0, -180, 0, -179)
    assert 110 < distance < 112

    # De 179 a 180
    distance = distance_km(0, 179, 0, 180)
    assert 110 < distance < 112
