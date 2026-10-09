"""Cortex Athlete API — application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="Cortex Athlete API",
    description="Tracks cognitive assessments and athletic performance sessions.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Report that the API process is running and able to serve requests."""
    return {"status": "ok"}