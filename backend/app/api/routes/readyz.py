from fastapi import APIRouter, status
from sqlalchemy import text

from app.api.deps import SessionDep
from app.core.responses import HealthJSONResponse
from app.schemas import ReadyCheckResponse

router = APIRouter(prefix="/readyz", tags=["health"])


@router.get(
    "",
    summary="Readiness check",
    description="Readiness check endpoint",
    response_class=HealthJSONResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Health check response",
            "content": {
                "application/health+json": {
                    "schema": ReadyCheckResponse.model_json_schema()
                }
            },
        },
    },
    openapi_extra={"security": []},
)
def readyz(session: SessionDep):
    try:
        session.execute(text("SELECT 1"))
    except Exception:
        return HealthJSONResponse(
            ReadyCheckResponse(
                status="fail",
                checks={"postgres:connections": [{"status": "fail"}]},
            ).model_dump(),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return HealthJSONResponse(
        ReadyCheckResponse(
            status="pass",
            checks={"postgres:connections": [{"status": "pass"}]},
        ).model_dump()
    )
