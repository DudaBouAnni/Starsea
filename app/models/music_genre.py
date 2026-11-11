"""Separa os metadados do provedor dos gêneros importados para cada usuário."""

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Integer, String, Table

from app.database.base import Base

artist_spotify_genre = Table(
    "artist_spotify_genre",
    Base.metadata,
    Column(
        "artist_id", Integer, ForeignKey("artists.artist_id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "genre_id", Integer, ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True
    ),
)

music_preference_genre = Table(
    "music_preference_genre",
    Base.metadata,
    Column("user_id", Integer, primary_key=True),
    Column("artist_id", Integer, primary_key=True),
    Column("source", String(30), primary_key=True),
    Column(
        "genre_id", Integer, ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True
    ),
    ForeignKeyConstraint(
        ["user_id", "artist_id", "source"],
        ["music_preferences.user_id", "music_preferences.artist_id", "music_preferences.source"],
        ondelete="CASCADE",
    ),
)
