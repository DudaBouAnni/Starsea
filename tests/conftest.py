import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SPOTIFY_CLIENT_ID"] = "test"
os.environ["SPOTIFY_CLIENT_SECRET"] = "test"
os.environ["SPOTIFY_REDIRECT_URI"] = "http://localhost/auth/callback"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.event import get_db as event_db
from app.api.user import get_db as user_db
from app.database.base import Base
from app.main import app
from app.models import Organizer, User


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine, autoflush=False)() as session:
        session.add_all(
            [
                Organizer(organizer_name="Produção"),
                User(username="Ana", email="ana@example.test"),
                User(username="Bia", email="bia@example.test"),
            ]
        )
        session.commit()
        yield session
    engine.dispose()


@pytest.fixture
def client(db):
    def override_db():
        yield db

    app.dependency_overrides[user_db] = override_db
    app.dependency_overrides[event_db] = override_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
