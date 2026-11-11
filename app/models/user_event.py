from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database.base import Base

"""
Tabela associativa entre usuário e evento.

Implementa a relação muitos para muitos entre usuários e eventos.
Cada registro representa a associação de um usuário a um evento.
"""
user_event = Table(
    "user_event",
    Base.metadata,
    # Identificador do usuário
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    # Identificador do evento
    Column("event_id", Integer, ForeignKey("events.event_id"), primary_key=True),
)
