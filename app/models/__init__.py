"""
Pacote de modelos do banco de dados Starsea.
Contém os modelos principais e tabelas associativas.
"""

from .user import User
from .event import Event
from .artist import Artist
from .genre import Genre
from .organizer import Organizer

# tabelas associativas
from .user_event import user_event
from .event_artist import event_artist
from .artist_genre import artist_genre
from .user_genre import user_genre
from .organizer_event import organizer_event