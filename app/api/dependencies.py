"""Dependências compartilhadas pelos módulos de rotas HTTP."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Fornece uma sessão do banco e garante seu fechamento ao final da requisição."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
