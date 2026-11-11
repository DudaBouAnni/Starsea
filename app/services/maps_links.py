"""Links públicos para abrir o local de um evento no Google Maps, sem chave de API."""

from urllib.parse import urlencode


def location_maps_url(
    latitude: float | None, longitude: float | None, address: str | None
) -> str | None:
    """Prioriza coordenadas; quando não houver, pesquisa pelo endereço cadastrado."""
    if latitude is not None and longitude is not None:
        query = f"{latitude},{longitude}"
    else:
        query = (address or "").strip()
    if not query:
        return None
    return "https://www.google.com/maps/search/?" + urlencode({"api": 1, "query": query})
