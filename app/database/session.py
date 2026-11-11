import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from app.database.config import PROJECT_ROOT, database_engine, is_local_database

load_dotenv(PROJECT_ROOT / ".env")

# URL de conexão com o banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Defina DATABASE_URL no arquivo .env.")
engine = database_engine(DATABASE_URL, os.getenv("CA_PATH"))
AUTO_CREATE_TABLES = is_local_database(DATABASE_URL)

# Cria a fábrica de sessões locais
SessionLocal = sessionmaker(
    autocommit=False,  # As alterações são persistidas somente após um commit explícito.
    autoflush=False,  # Desativa o envio automático de alterações pendentes ao banco.
    bind=engine,  # Vincula a sessão ao mecanismo de conexão criado.
)
