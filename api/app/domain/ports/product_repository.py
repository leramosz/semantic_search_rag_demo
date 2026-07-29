"""Repository port definitions for product retrieval operations."""

from typing import Protocol

from app.domain.models.product import ProductSearchHit


class ProductRepositoryPort(Protocol):
    """Define the contract for semantic product retrieval.

    Infrastructure adapters must implement this port to retrieve products
    from the persistence layer.
    """

    def search_by_vector(self, query_vector: str, top_k: int, ef_search: int) -> list[ProductSearchHit]:
        """Return the top matching products for the given vector.

        Args:
            query_vector: pgvector-compatible string representation.
            top_k: Maximum number of search hits to return.
            ef_search: HNSW search breadth parameter.

        Returns:
            A ranked list of product search hits.
        """
