import random
import re
import string
import uuid

from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.models import ShortURL, ShortURLStats
from app.schemas import ShortURLCreate, ShortURLCreateResponse
from app.utils import validate_url

router = APIRouter(prefix="/shorten", tags=["shorten"])

# Characters allowed for random shortcode generation
RANDOM_SHORTCODE_CHARS = string.ascii_letters + string.digits + "_"


def generate_random_shortcode() -> str:
    """
    Generate a random shortcode of 6 characters.

    This function creates a random string composed of characters from
    `RANDOM_SHORTCODE_CHARS`.

    Returns:
        str: A randomly generated shortcode string.
    """
    return "".join(random.choices(RANDOM_SHORTCODE_CHARS, k=6))


def validate_shortcode(shortcode: str) -> str:
    """
    Validates that the shortcode contains only characters allowed in the path
    portion of a URL.

    Allowed characters are the unreserved characters as per RFC 3986:
    ALPHA / DIGIT / "-" / "." / "_" / "~"

    Args:
        shortcode (str): The shortcode to validate.

    Returns:
        str: The valid shortcode.

    Raises:
        ValueError: If the shortcode contains invalid characters.
    """
    pattern = re.compile(r"^[A-Za-z0-9\-._~]+$")

    if pattern.fullmatch(shortcode) and shortcode not in [
        "openapi.json",
        "redoc",
        "docs",
    ]:
        return shortcode
    else:
        raise ValueError("The provided shortcode is invalid")


@router.post(
    "",
    response_model=ShortURLCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Shorten a URL",
    description="Shorten a URL to a 6-character or custom shortcode",
    responses={
        400: {"description": "Url not present"},
        409: {"description": "Shortcode already in use"},
        412: {"description": "The provided shortcode/url is invalid"},
    },
    openapi_extra={"security": []},
)
def shorten(request: ShortURLCreate, session: SessionDep) -> ShortURLCreateResponse:
    # Use provided shortcode or generate one
    shortcode = request.shortcode or generate_random_shortcode()

    # Keep generating shortcodes if the generated one already exists
    #
    # The faster way to do this at scale is probably to use a bloom filter
    # index, though, at scale, it's also probably better to rethink permanent
    # 6-character shortcodes.
    if not request.shortcode:
        while True:
            if not session.query(ShortURL).filter_by(shortcode=shortcode).first():
                break
            else:
                shortcode = generate_random_shortcode()
                continue

    if not request.url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Url not present"
        )

    try:
        validate_url(request.url)
        shortcode = validate_shortcode(shortcode)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="The provided shortcode/url is invalid",
        )

    # Check if shortcode already exists
    existing = session.query(ShortURL).filter_by(shortcode=shortcode).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Shortcode already in use",
        )

    # Generate a unique update_id
    update_id = uuid.uuid4()

    # Store the mapping with update_id
    new_shortcode = ShortURL(
        url=str(request.url), shortcode=shortcode, update_id=update_id
    )

    # Store the shortcode with creation timestamp
    new_shortcode_stats = ShortURLStats(shortcode=shortcode)

    session.add(new_shortcode)
    session.add(new_shortcode_stats)
    session.commit()
    session.refresh(new_shortcode)
    session.refresh(new_shortcode_stats)

    return ShortURLCreateResponse(shortcode=shortcode, update_id=update_id)
