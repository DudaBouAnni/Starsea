from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

#URL do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

#Criando conexão com o banco de dados
engine = create_engine(DATABASE_URL)

#Criando nova sessão local
SessionLocal = sessionmaker(
    autocommit=False, #Garante que as alterações só sejam salvas quando houver commit
    autoflush=False, #Evita flush automático, controla quando dados são enviados ao banco
    bind=engine #Víncula a sessão a engine criada
)