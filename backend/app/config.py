import os

# Frontend origins allowed to read API responses from a browser.
# Comma-separated. Defaults to the Vite dev server; production sets CORS_ORIGINS.
DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"


def get_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)
    return [origin.strip() for origin in raw.split(",") if origin.strip()]