from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import RedirectResponse

from app.api.deps import SessionDep
from app.models import ShortURL, ShortURLStats

router = APIRouter(prefix="", tags=[""])


def increment_redirect_count(shortcode: str, session: SessionDep) -> None:
    """
    Increment the redirect count and update the last redirect timestamp for a
    given shortcode.

    Args:
        shortcode (str): The shortcode identifier of the URL to update
        session (SessionDep): The database session dependency for executing
                              queries

    Returns:
        None

    Note:
        This function performs an atomic update operation that:
        - Increments the redirect_count by 1
        - Updates the last_redirect timestamp to current UTC time
    """
    session.query(ShortURLStats).filter_by(shortcode=shortcode).update(
        {
            "redirect_count": ShortURLStats.redirect_count + 1,
            "last_redirect": datetime.utcnow(),
        }
    )
    session.commit()


@router.get(
    "/{shortcode}",
    status_code=status.HTTP_302_FOUND,
    summary="Redirect to original URL",
    description="Redirects to the original URL based on the provided shortcode.",
    responses={404: {"description": "Shortcode not found"}},
)
async def redirect(
    shortcode: str, session: SessionDep, background_tasks: BackgroundTasks
) -> RedirectResponse:
    record = session.query(ShortURL).filter_by(shortcode=shortcode).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shortcode not found.",
        )

    background_tasks.add_task(increment_redirect_count, shortcode, session)
    return RedirectResponse(url=record.url, status_code=status.HTTP_302_FOUND)
