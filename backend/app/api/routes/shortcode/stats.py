from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.models import ShortURLStats
from app.schemas import ShortURLStatsResponse

router = APIRouter(prefix="", tags=[""])


@router.get(
    "/{shortcode}/stats",
    response_model=ShortURLStatsResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Shortcode not found"}},
    openapi_extra={"security": []},
)
def stats(shortcode: str, session: SessionDep) -> ShortURLStatsResponse:
    if not shortcode:
        # Should never be reached due to route
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shortcode not found"
        )

    record = session.query(ShortURLStats).filter_by(shortcode=shortcode).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shortcode not found"
        )

    return ShortURLStatsResponse(
        created=record.created_at,
        lastRedirect=record.last_redirect,
        redirectCount=record.redirect_count,
    )
