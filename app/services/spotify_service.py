import requests

from app.core.settings import settings


def get_spotify_login_url():
    return (
        "https://accounts.spotify.com/authorize"
        f"?client_id={settings.SPOTIFY_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={settings.SPOTIFY_REDIRECT_URI}"
        "&scope=user-read-email user-read-private"
    )

def get_access_token(code: str):
    token_url = "https://accounts.spotify.com/api/token"

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(token_url, data=token_data)

    return response.json()

def get_spotify_user(access_token: str):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        "https://api.spotify.com/v1/me",
        headers=headers,
    )

    return response.json()