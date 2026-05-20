from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str

    class Config:
        env_file = ".env"

settings = Settings()