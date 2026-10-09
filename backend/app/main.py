"""Cortex Athlete API — application entry point."""

from fastapi import FastAPI

from app.routers import health

app = FastAPI(
    title="Cortex Athlete API",
    description="Tracks cognitive assessments and athletic performance sessions.",
    version="0.1.0",
)

app.include_router(health.router)