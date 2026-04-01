from fastapi import FastAPI

from app.database.session import engine
from app.database.base import Base
from app.api.user import router as users_router
from app.api.event import router as events_router
from app.api.artist import router as artists_router
from app.api.genre import router as genres_router
from app.api.organizer import router as organizers_router

"""
Main da API Starsea.

Responsável por:
- Inicializar a aplicação FastAPI
- Criar as tabelas no banco de dados (se não existirem)
- Registrar os routers de cada recurso (usuários, eventos, artistas, gêneros, organizadores)
- Fornecer endpoint de health check
"""

#Cria instância do FastAPI
app = FastAPI(
    title="Starsea API",
    description="API para gerenciamento das entidades do Starsea",
    version="1.0.0"
)

#Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

#Registra os routers
app.include_router(users_router)
app.include_router(events_router)
app.include_router(artists_router)
app.include_router(genres_router)
app.include_router(organizers_router)

#Health check
@app.get("/", summary="Verifica se API está rodando", response_description="Status da API")
def health_check():
    """
       Endpoint de health check da aplicação.

       Retorna:
        - status: indica se a API está online
    """
    return {"status": "ok"}