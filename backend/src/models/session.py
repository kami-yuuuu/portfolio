from sqlmodel import SQLModel, create_engine
from . import category, transaction, payment_method  # noqa: F401

from config import get_database_url, get_sql_echo

DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=get_sql_echo(), pool_pre_ping=True)


def create_db_and_tables():
    """Deprecated compatibility helper; use Alembic migrations for schema changes."""
    SQLModel.metadata.create_all(engine)


def delete_db_and_tables():
    """Dangerous legacy helper retained for compatibility; do not use in production."""
    SQLModel.metadata.drop_all(engine)


if __name__ == "__main__":
    import sys

    if "create" in sys.argv:
        create_db_and_tables()
    elif "delete" in sys.argv:
        delete_db_and_tables()
    else:
        print("Usage: python -m models.session [create|delete]")
