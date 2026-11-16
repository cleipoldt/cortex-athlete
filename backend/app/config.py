import os
from pathlib import Path

# Frontend origins allowed to read API responses from a browser.
# Comma-separated. Defaults to the Vite dev server; production sets CORS_ORIGINS.
DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"


def get_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


# The backend/ folder, found from this file's location (backend/app/config.py).
BACKEND_DIR = Path(__file__).resolve().parent.parent

# Development default: a SQLite file at backend/cortex.db.
# Production sets DATABASE_URL to a PostgreSQL connection string instead.
DEFAULT_DATABASE_URL = f"sqlite:///{(BACKEND_DIR / 'cortex.db').as_posix()}"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)