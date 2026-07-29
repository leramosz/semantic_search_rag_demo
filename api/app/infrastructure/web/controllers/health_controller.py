"""HTTP controller exposing health check endpoints."""

from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Return a simple liveness status for the API.

    Returns:
        A dictionary with the service status.
    """
    return {"status": "ok"}
