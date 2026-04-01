from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#URL da conexão local com mysql (teste)
DATABASE_URL = "mysql+pymysql://root:toor@localhost/starsea"

#Criando conexão com o banco de dados
engine = create_engine(DATABASE_URL)

#Criando nova sessão local
SessionLocal = sessionmaker(
    autocommit=False, #Garante que as alterações só sejam salvas quando houver commit
    autoflush=False, #Evita flush automático, controla quando dados são enviados ao banco
    bind=engine #Víncula a sessão a engine criada
)