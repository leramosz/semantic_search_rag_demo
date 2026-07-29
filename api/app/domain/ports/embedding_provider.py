"""Embedding provider port definitions."""

from typing import Protocol


class EmbeddingProviderPort(Protocol):
    """Define the contract for generating query embeddings."""

    def embed_query(self, query: str) -> list[float]:
        """Generate an embedding vector for a user query.

        Args:
            query: User query text.

        Returns:
            A numeric embedding vector.
        """
