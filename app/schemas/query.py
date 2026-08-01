from datetime import datetime

from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    source_type: str
    original_source: str | None = None
    created_at: datetime
    snippet: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]