"""Database connection helpers for PostgreSQL access."""

import psycopg2

from app.infrastructure.config.settings import Settings


class PostgresConnectionFactory:
    """Create PostgreSQL connections for repository adapters."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the connection factory with application settings.

        Args:
            settings: Resolved application settings.
        """
        self._settings = settings

    def create_connection(self):
        """Create a new psycopg2 connection.

        Returns:
            A psycopg2 connection instance.
        """
        return psycopg2.connect(
            host=self._settings.db_host,
            port=self._settings.db_port,
            dbname=self._settings.db_name,
            user=self._settings.db_user,
            password=self._settings.db_password,
        )
