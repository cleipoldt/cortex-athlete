from collections.abc import Iterator

from sqlalchemy import MetaData, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_database_url

DATABASE_URL = get_database_url()
IS_SQLITE = DATABASE_URL.startswith("sqlite")

# SQLite only: let FastAPI's worker threads share the connection.
connect_args = {"check_same_thread": False} if IS_SQLITE else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)


def enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    """Turn on foreign key enforcement for a new SQLite connection.

    SQLite ignores foreign keys unless every connection opts in. This is a
    named function (not tied to one engine) so the test engine can reuse it.
    Deliberately NOT applied to Alembic's engine: SQLite migrations rebuild
    tables by dropping them, and with foreign keys on, ON DELETE CASCADE
    would wipe child rows during that rebuild.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


if IS_SQLITE:
    event.listen(engine, "connect", enable_sqlite_foreign_keys)


# Factory that creates a new session (one per request).
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db() -> Iterator[Session]:
    """FastAPI dependency: one database session per request, always closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Every constraint gets a predictable name, identical on SQLite and PostgreSQL,
# so future migrations can find it by name.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Parent class for every model. Alembic reads its registry of tables."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)