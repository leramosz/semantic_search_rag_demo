"""Domain models used by semantic search and RAG use cases."""

from dataclasses import dataclass


@dataclass(slots=True)
class ProductSearchHit:
    """Represent a ranked product returned by semantic search.

    This model is the core domain representation shared across the
    repository, service, and web layers.
    """

    id: int
    name: str | None
    short_description: str | None
    ingredients_text: str | None
    url: str | None
    raw_text: str
    similarity: float
