from __future__ import annotations

import os


def get_database_url() -> str:
    """Return the configured database URL, failing fast when it is missing."""
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL must be set before starting the application")
    if url.startswith("postgres://"):
        url = "postgresql://" + url.removeprefix("postgres://")
    return url


def get_sql_echo() -> bool:
    return os.getenv("SQL_ECHO", "false").strip().lower() in {"1", "true", "yes"}
