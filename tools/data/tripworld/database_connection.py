"""Environment-only credentials and transactional, checksum-verified SQL migrations."""

import hashlib
import os
from contextlib import contextmanager
from pathlib import Path

import psycopg
from psycopg.rows import dict_row


class TripWorldDatabaseError(RuntimeError):
    """Sanitized database error; connection strings and credentials are never logged."""


@contextmanager
def connection():
    try:
        password = os.environ.get("TRIPWORLD_DB_PASSWORD")
        if not password:
            raise TripWorldDatabaseError("Set TRIPWORLD_DB_PASSWORD in the environment")
        with psycopg.connect(
            host=os.environ.get("TRIPWORLD_DB_HOST", "127.0.0.1"),
            port=os.environ.get("TRIPWORLD_DB_PORT", "55432"),
            dbname=os.environ.get("TRIPWORLD_DB_NAME", "tripworld"),
            user=os.environ.get("TRIPWORLD_DB_USER", "tripworld"),
            password=password,
            connect_timeout=10,
            row_factory=dict_row,
        ) as conn:
            conn.execute("SET statement_timeout = '15min'")
            yield conn
    except psycopg.Error as exc:
        raise TripWorldDatabaseError(
            f"TripWorld database operation failed ({type(exc).__name__}, SQLSTATE={exc.sqlstate})"
        ) from None


def migrate(conn, directory: Path | None = None) -> list[str]:
    directory = directory or Path(__file__).with_name("migrations")
    applied = []
    with conn.transaction():
        conn.execute("SELECT pg_advisory_xact_lock(74501901)")
        conn.execute("CREATE SCHEMA IF NOT EXISTS tripworld")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tripworld.schema_migrations "
            "(version text PRIMARY KEY, checksum text NOT NULL, "
            "applied_at timestamptz NOT NULL DEFAULT now())"
        )
        for path in sorted(directory.glob("*.sql")):
            checksum = hashlib.sha256(path.read_bytes()).hexdigest()
            row = conn.execute(
                "SELECT checksum FROM tripworld.schema_migrations WHERE version=%s", (path.name,)
            ).fetchone()
            if row:
                if row["checksum"] != checksum:
                    raise ValueError("Applied migration checksum mismatch")
                continue
            conn.execute(path.read_text(encoding="utf-8"))
            conn.execute(
                "INSERT INTO tripworld.schema_migrations(version,checksum) VALUES (%s,%s)",
                (path.name, checksum),
            )
            applied.append(path.name)
    return applied
