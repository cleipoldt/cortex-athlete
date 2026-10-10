"""Cortex Athlete API — application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_cors_origins
from app.routers import health

app = FastAPI(
    title="Cortex Athlete API",
    description="Tracks cognitive assessments and athletic performance sessions.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)