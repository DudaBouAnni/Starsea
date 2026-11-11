from datetime import datetime
from math import asin, cos, radians, sin, sqrt
from zoneinfo import ZoneInfo


def local_today():
    return datetime.now(ZoneInfo("America/Sao_Paulo")).date()


def has_coordinates(entity):
    return entity.latitude is not None and entity.longitude is not None


def distance_km(latitude_a, longitude_a, latitude_b, longitude_b):
    """Calcula a distância sobre a esfera terrestre, e não a distância de um trajeto por vias."""
    lat_a, lon_a, lat_b, lon_b = map(radians, (latitude_a, longitude_a, latitude_b, longitude_b))
    haversine = (
        sin((lat_b - lat_a) / 2) ** 2 + cos(lat_a) * cos(lat_b) * sin((lon_b - lon_a) / 2) ** 2
    )
    return 6371.0088 * 2 * asin(sqrt(min(1, max(0, haversine))))
