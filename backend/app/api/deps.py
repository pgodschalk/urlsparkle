from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine


def get_db() -> Generator[Session, None, None]:
    """
    Creates and yields a database session.

    This dependency function creates a new SQLAlchemy Session instance, yields
    it for use in FastAPI endpoints, and automatically closes the session when
    the request is complete.

    Yields:
        Session: A SQLAlchemy database session object.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
