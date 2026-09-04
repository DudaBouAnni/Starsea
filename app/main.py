from fastapi import FastAPI

from app.database.session import engine
from app.database.base import Base
from app.api.user import router as users_router
from app.api.event import router as events_router
from app.api.artist import router as artists_router
from app.api.genre import router as genres_router
from app.api.auth import router as auth_router
from app.api.organizer import router as organizers_router

"""
Main file of the Starsea API

Responsible for:
- Initializing the FastAPI application
- Creating database tables if they do not exist
- Registering routers for each resource (users, events, artists, genres, organizers)
- Providing a health check endpoint
"""

#Creates the FastAPI instance
app = FastAPI(
    title="Starsea API",
    description="API for managing Starsea entities",
    version="1.0.0"
)

#Creates the database tables
Base.metadata.create_all(bind=engine)

#Register the routers
app.include_router(users_router)
app.include_router(events_router)
app.include_router(artists_router)
app.include_router(genres_router)
app.include_router(organizers_router)
app.include_router(auth_router)

#Health check
@app.get("/", summary="Checks if the API is running", response_description="Status da API")
def health_check():
    """
       Application health check endpoint

       Returns:
        - status: indicates wheather the API is online
    """
    return {"status": "ok"}