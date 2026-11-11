"""
Execute antes de iniciar uma instalação existente: python -m app.database.migrate_nearby.

Migração aditiva e repetível para MySQL/SQLite. Faça backup do banco antes de executar.
O MySQL pode confirmar DDL implicitamente; esta migração não desfaz alterações automaticamente.
"""

from sqlalchemy import inspect, text

import app.models  # Registra todas as tabelas antes de executar create_all.
from app.database.base import Base
from app.database.session import engine


def migrate(connection):
    additions = {
        "users": {
            "latitude": "FLOAT NULL",
            "longitude": "FLOAT NULL",
            "notification_radius_km": "FLOAT NOT NULL DEFAULT 50",
            "nearby_notifications_enabled": "BOOLEAN NOT NULL DEFAULT TRUE",
        },
        "events": {"latitude": "FLOAT NULL", "longitude": "FLOAT NULL"},
    }
    inspector = inspect(connection)
    for table, columns in additions.items():
        if not inspector.has_table(table):
            continue
        existing = {column["name"] for column in inspector.get_columns(table)}
        for name, definition in columns.items():
            if name not in existing:
                # Os identificadores e as definições são constantes deste módulo.
                connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {definition}"))
    Base.metadata.create_all(connection)


if __name__ == "__main__":
    with engine.begin() as connection:
        migrate(connection)
    print("Migração de localização e notificações concluída.")
