from sqlalchemy import MetaData, create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_database_url

DATABASE_URL = get_database_url()
IS_SQLITE = DATABASE_URL.startswith("sqlite")

# SQLite only: let FastAPI's worker threads share the connection.
connect_args = {"check_same_thread": False} if IS_SQLITE else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SQLite ignores foreign keys unless every connection turns them on.
if IS_SQLITE:

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Factory that creates a new session (one per request).
SessionLocal = sessionmaker(bind=engine, autoflush=False)

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