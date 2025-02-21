from fastapi import APIRouter, status

from app.core.responses import HealthJSONResponse
from app.schemas import HealthCheckResponse

router = APIRouter(prefix="/healthz", tags=["health"])


@router.get(
    "",
    summary="Health check",
    description="Health check endpoint",
    response_class=HealthJSONResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Health check response",
            "content": {
                "application/health+json": {
                    "schema": HealthCheckResponse.model_json_schema()
                }
            },
        }
    },
    openapi_extra={"security": []},
)
def healthz():
    return HealthJSONResponse(
        HealthCheckResponse(status="pass").model_dump(),
        media_type="application/health+json",
    )
