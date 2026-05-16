from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

#Database URL
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

#Creating connection to the database
engine = create_engine(DATABASE_URL)

#Creating new local session
SessionLocal = sessionmaker(
    autocommit=False, #Ensures that changes are only saved when a commit occurs
    autoflush=False, #Prevents automatic flush; controls when data is sent to the database
    bind=engine #Binds the session to the created engine
)