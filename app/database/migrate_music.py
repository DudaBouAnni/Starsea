"""
Adiciona preferências musicais sem remover os dados existentes.

Execute: python -m app.database.migrate_music. Aplica também a migração de proximidade.
Faça backup antes de alterar bancos de produção: o MySQL pode confirmar DDL implicitamente.
"""

from sqlalchemy import inspect, text

from app.database.migrate_nearby import migrate as migrate_nearby
from app.database.session import engine


def migrate(connection):
    migrate_nearby(connection)
    additions = {
        "users": {
            "personalized_notifications_only": "BOOLEAN NOT NULL DEFAULT FALSE",
            "spotify_preferences_synced_at": "DATETIME NULL",
        },
        "artists": {"spotify_id": "VARCHAR(255) NULL"},
    }
    for table, columns in additions.items():
        existing = {column["name"] for column in inspect(connection).get_columns(table)}
        for name, definition in columns.items():
            if name not in existing:
                connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {definition}"))
    inspector = inspect(connection)
    unique_definitions = inspector.get_unique_constraints("artists") + [
        index for index in inspector.get_indexes("artists") if index.get("unique")
    ]
    if not any(item["column_names"] == ["spotify_id"] for item in unique_definitions):
        connection.execute(
            text("CREATE UNIQUE INDEX uq_artists_spotify_id ON artists (spotify_id)")
        )


if __name__ == "__main__":
    with engine.begin() as connection:
        migrate(connection)
    print("Migração do perfil musical concluída.")
