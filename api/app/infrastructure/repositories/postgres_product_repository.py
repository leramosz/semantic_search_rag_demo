"""PostgreSQL repository adapter for product retrieval."""

from app.domain.models.product import ProductSearchHit
from app.domain.ports.product_repository import ProductRepositoryPort
from app.infrastructure.database.connection import PostgresConnectionFactory


class PostgresProductRepository(ProductRepositoryPort):
    """Retrieve product search hits from PostgreSQL using pgvector."""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        """Initialize the repository with a connection factory.

        Args:
            connection_factory: Factory used to create PostgreSQL connections.
        """
        self._connection_factory = connection_factory

    def search_by_vector(self, query_vector: str, top_k: int, ef_search: int) -> list[ProductSearchHit]:
        """Return the top matching products for the given vector.

        Args:
            query_vector: pgvector-compatible string representation.
            top_k: Maximum number of search hits to return.
            ef_search: HNSW search breadth parameter.

        Returns:
            A ranked list of product search hits.
        """
        conn = self._connection_factory.create_connection()
        conn.autocommit = False

        try:
            with conn.cursor() as cur:
                cur.execute("BEGIN;")
                cur.execute("SET LOCAL hnsw.ef_search = %s;", (ef_search,))
                cur.execute(
                    """
                    SELECT
                        id,
                        name,
                        short_description,
                        ingredients_text,
                        url,
                        raw_text,
                        1 - (embedding <=> %s::vector) AS similarity
                    FROM products
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s;
                    """,
                    (query_vector, query_vector, top_k),
                )
                rows = cur.fetchall()
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

        return [
            ProductSearchHit(
                id=row[0],
                name=row[1],
                short_description=row[2],
                ingredients_text=row[3],
                url=row[4],
                raw_text=row[5],
                similarity=float(row[6]),
            )
            for row in rows
        ]
