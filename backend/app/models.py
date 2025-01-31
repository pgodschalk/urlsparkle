import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Text, func
from sqlalchemy.types import DateTime
from sqlmodel import Field, SQLModel


class ShortURLBase(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    shortcode: str = Field(unique=True, index=True, nullable=False, sa_type=Text)


# Database model, database table inferred from class name
#
# Avoids using the API's `update_id` as the primary key. Mainly done so if,
# for any reason, the UUID is compromised, it can be changed without having
# to change the PK.
class ShortURL(ShortURLBase, table=True):
    url: str = Field(index=True, nullable=False, sa_type=Text)
    update_id: uuid.UUID = Field(index=True, unique=True, nullable=False)


# This is intentionally separated out, so that we in the future could have the
# timestamps entirely handled by the database engine, rather than the
# application server by using triggers on simply checking if the row is
# updated, rather than a column.
class ShortURLStats(ShortURLBase, table=True):
    created_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
    )
    last_redirect: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    redirect_count: int = Field(
        default=0,
        nullable=False,
    )
