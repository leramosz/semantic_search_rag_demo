"""DTOs for RAG chat HTTP requests and responses."""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Represent the payload required to perform grounded chat generation."""

    query: str = Field(..., min_length=1, description="User question")
    top_k: int = Field(default=5, ge=1, le=10)


class AskSourceResponse(BaseModel):
    """Represent a source item used to ground the chat answer."""

    id: int
    name: str | None = None
    url: str | None = None
    similarity: float


class AskResponse(BaseModel):
    """Represent the grounded chat API response payload."""

    query: str
    top_k: int
    answer: str
    sources: list[AskSourceResponse]
