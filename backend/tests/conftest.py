"""Shared pytest fixtures: an isolated test database for every test.

Each test gets a brand-new SQLite file in a temporary folder, so tests never
touch the development database (backend/cortex.db) and never affect each other.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

import app.models  # noqa: F401  (registers every table on Base.metadata)
from app.database import Base, enable_sqlite_foreign_keys, get_db
from app.main import app
from app.models import User


@pytest.fixture
def test_session_factory(tmp_path) -> Iterator[sessionmaker[Session]]:
    """Create a fresh database file with every table, plus the dev user (id 1)."""
    engine = create_engine(
        f"sqlite:///{(tmp_path / 'test.db').as_posix()}",
        connect_args={"check_same_thread": False},
    )
    event.listen(engine, "connect", enable_sqlite_foreign_keys)
    Base.metadata.create_all(engine)

    factory = sessionmaker(bind=engine, autoflush=False)

    with factory() as session:
        session.add(User(id=1, email="test@example.com", display_name="Test Athlete"))
        session.commit()

    yield factory

    engine.dispose()


@pytest.fixture
def db_session(test_session_factory) -> Iterator[Session]:
    """A session for a test to inspect the database directly."""
    with test_session_factory() as session:
        yield session


@pytest.fixture
def client(test_session_factory) -> Iterator[TestClient]:
    """An HTTP test client whose endpoints use the test database."""

    def override_get_db() -> Iterator[Session]:
        with test_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()