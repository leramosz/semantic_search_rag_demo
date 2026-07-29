"""Application service responsible for semantic product retrieval."""

from app.domain.models.product import ProductSearchHit
from app.domain.ports.embedding_provider import EmbeddingProviderPort
from app.domain.ports.product_repository import ProductRepositoryPort


class SemanticSearchService:
    """Execute semantic search use cases.

    This service coordinates query embedding generation and vector-based
    product retrieval from the repository layer.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProviderPort,
        product_repository: ProductRepositoryPort,
        ef_search: int,
    ) -> None:
        """Initialize the service with its dependencies.

        Args:
            embedding_provider: Adapter used to embed user queries.
            product_repository: Adapter used to query PostgreSQL.
            ef_search: HNSW ef_search value used during vector retrieval.
        """
        self._embedding_provider = embedding_provider
        self._product_repository = product_repository
        self._ef_search = ef_search

    def search(self, query: str, top_k: int) -> list[ProductSearchHit]:
        """Search products semantically for the given query.

        Args:
            query: User search text.
            top_k: Maximum number of results to return.

        Returns:
            A ranked list of product search hits.

        Raises:
            ValueError: If the query is blank after trimming.
        """
        normalized_query = query.strip()
        if not normalized_query:
            raise ValueError("query cannot be empty")

        embedding = self._embedding_provider.embed_query(normalized_query)
        query_vector = self._vector_to_pg(embedding)
        return self._product_repository.search_by_vector(query_vector, top_k, self._ef_search)

    @staticmethod
    def _vector_to_pg(values: list[float]) -> str:
        """Convert a Python vector to the pgvector string representation.

        Args:
            values: Embedding values to convert.

        Returns:
            A pgvector-compatible string.
        """
        return "[" + ",".join(str(v) for v in values) + "]"
