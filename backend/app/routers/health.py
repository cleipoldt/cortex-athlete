from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """Report that the API process is running and able to serve requests."""
    return {"status": "ok"}