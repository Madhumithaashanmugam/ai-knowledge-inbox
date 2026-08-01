from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class SourceType(str, Enum):
    text = "text"
    url = "url"


class ItemCreate(BaseModel):
    source_type: SourceType
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value, info):
        source_type = info.data.get("source_type")

        if not value.strip():
            raise ValueError("Content cannot be empty.")

        if source_type == SourceType.url:
            if not (
                value.startswith("http://")
                or value.startswith("https://")
            ):
                raise ValueError(
                    "Please enter a valid URL starting with http:// or https://"
                )

        return value


class ItemResponse(BaseModel):
    id: int
    source_type: SourceType
    original_source: str | None = None

    # AI Generated
    title: str | None = None
    summary: str | None = None

    # Original content
    content: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)