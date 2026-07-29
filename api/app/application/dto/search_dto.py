"""DTOs for semantic search HTTP requests and responses."""

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Represent the payload required to perform semantic search."""

    query: str = Field(..., min_length=1, description="Search text")
    top_k: int = Field(default=10, ge=1, le=50)


class SearchResultResponse(BaseModel):
    """Represent a single semantic search result in the API response."""

    id: int
    name: str | None = None
    short_description: str | None = None
    url: str | None = None
    raw_text: str
    similarity: float


class SearchResponse(BaseModel):
    """Represent the semantic search API response payload."""

    query: str
    top_k: int
    results: list[SearchResultResponse]
