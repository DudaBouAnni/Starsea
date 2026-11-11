"""
Pacote de modelos do banco de dados Starsea.

Contém os modelos principais e as tabelas associativas.
"""

from .artist import Artist
from .artist_genre import artist_genre
from .event import Event
from .event_artist import event_artist
from .genre import Genre
from .music_genre import artist_spotify_genre, music_preference_genre
from .music_preference import MusicPreference
from .notification import Notification
from .organizer import Organizer
from .organizer_event import organizer_event
from .user import User

# tabelas associativas
from .user_event import user_event
from .user_genre import user_genre
