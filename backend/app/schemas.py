import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


# Properties to receive via API on creation
class ShortURLCreate(BaseModel):
    # Intentionally doesn't use pydantic's HttpUrl so we can use our own
    # validation instead
    url: str
    shortcode: Optional[str] = Field(None)

    model_config = {
        "json_schema_extra": {
            "examples": [{"url": "https://www.example.com", "shortcode": "abn123"}]
        }
    }


# Properties to return to the client on creation
class ShortURLCreateResponse(BaseModel):
    shortcode: str
    update_id: uuid.UUID


# Properties to receive via API on update
class ShortURLUpdate(BaseModel):
    # Intentionally doesn't use pydantic's HttpUrl so we can use our own
    # validation instead
    url: str

    model_config = {
        "json_schema_extra": {"examples": [{"url": "https://www.example.com"}]}
    }


# Properties to return to the client on update
class ShortURLUpdateResponse(BaseModel):
    shortcode: str

    model_config = {"json_schema_extra": {"examples": [{"shortcode": "abn123"}]}}


# Properties to return via API
class ShortURLPublic(BaseModel):
    url: HttpUrl


# Properties to return via API
class ShortURLStatsResponse(BaseModel):
    created: datetime
    lastRedirect: Optional[datetime]
    redirectCount: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "created": "2017-05-10T20:45:00.000Z",
                    "lastRedirect": "2018-05-16T10:16:24.666Z",
                    "redirect_count": 6,
                }
            ]
        }
    }
