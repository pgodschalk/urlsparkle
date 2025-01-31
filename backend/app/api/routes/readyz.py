from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from app.api.deps import SessionDep

router = APIRouter(prefix="/readyz", tags=["health"])


@router.head(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Readiness check",
    description="Readiness check endpoint",
)
def readyz(session: SessionDep):
    try:
        session.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed {e}",
        )
    return None
