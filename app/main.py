"""
Arquivo principal da API Starsea.

Responsável por:
- Inicializar a aplicação FastAPI.
- Criar as tabelas que ainda não existem.
- Registrar as rotas de usuários, eventos, artistas, gêneros e organizadores.
- Disponibilizar uma rota para verificar o funcionamento da API.
"""

from fastapi import FastAPI

from app.api.router import API_ROUTERS
from app.database.base import Base
from app.database.session import engine

# Cria a instância do FastAPI
app = FastAPI(title="Starsea API", description="API for managing Starsea entities", version="1.0.0")

# Cria as tabelas que ainda não existem no banco
Base.metadata.create_all(bind=engine)

# Registra as rotas da aplicação
for router in API_ROUTERS:
    app.include_router(router)


# Verifica se a API está disponível
@app.get("/", summary="Checks if the API is running", response_description="Status da API")
def health_check():
    """
    Verifica se a aplicação está disponível.

    Retorna:
    - **status**: indica se a API está em funcionamento.
    """
    return {"status": "ok"}
