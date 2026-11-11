import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# URL de conexão com o banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Cria a fábrica de sessões locais
SessionLocal = sessionmaker(
    autocommit=False,  # As alterações são persistidas somente após um commit explícito.
    autoflush=False,  # Desativa o envio automático de alterações pendentes ao banco.
    bind=engine,  # Vincula a sessão ao mecanismo de conexão criado.
)
