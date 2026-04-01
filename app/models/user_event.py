from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

"""
Tabela associativa entre User e Event.

Responsável por implementar a relação many-to-many entre usuários e eventos.
Cada registro representa a associação entre um usuário e um evento.
"""
user_event = Table(

    "user_event",
    Base.metadata,
    #ID do usuário
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    #ID do evento
    Column("event_id", Integer, ForeignKey("events.event_id"), primary_key=True)
)