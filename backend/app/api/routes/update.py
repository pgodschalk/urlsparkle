from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.models import ShortURL
from app.schemas import ShortURLUpdate, ShortURLUpdateResponse
from app.utils import validate_url

router = APIRouter(prefix="/update", tags=["update"])


@router.post(
    "/{update_id}",
    response_model=ShortURLUpdateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Update a URL",
    description="Update the URL associated with a given update ID.",
    responses={
        400: {"description": "Url not present"},
        401: {"description": "The provided update ID does not exist"},
        412: {"description": "The provided url is invalid"},
    },
)
def update_url(
    request: ShortURLUpdate, session: SessionDep, update_id: str
) -> ShortURLUpdateResponse:
    if not request.url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Url not present",
        )

    try:
        validate_url(request.url)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=str(e),
        )

    record = session.query(ShortURL).filter_by(update_id=update_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The provided update ID does not exist",
        )

    # Update the mapping with the new URL
    record.url = str(request.url)
    session.commit()
    session.refresh(record)

    return ShortURLUpdateResponse(shortcode=record.shortcode)
