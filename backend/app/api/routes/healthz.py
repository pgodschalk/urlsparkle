from fastapi import APIRouter, status

router = APIRouter(prefix="/healthz", tags=["health"])


@router.head(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Health check",
    description="Health check endpoint",
)
def healthz():
    return None
