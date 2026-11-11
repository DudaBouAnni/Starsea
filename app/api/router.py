"""Rotas da aplicação na ordem original de registro."""

from app.api.artist import router as artists_router
from app.api.auth import router as auth_router
from app.api.event import router as events_router
from app.api.genre import router as genres_router
from app.api.music import router as music_router
from app.api.nearby import router as nearby_router
from app.api.organizer import router as organizers_router
from app.api.user import router as users_router

API_ROUTERS = (
    users_router,
    events_router,
    artists_router,
    genres_router,
    organizers_router,
    auth_router,
    nearby_router,
    music_router,
)
