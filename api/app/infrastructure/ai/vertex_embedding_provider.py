"""Vertex AI adapter for embedding generation."""

from google import genai
from google.genai import types

from app.domain.ports.embedding_provider import EmbeddingProviderPort
from app.infrastructure.config.settings import Settings


class VertexEmbeddingProvider(EmbeddingProviderPort):
    """Generate embeddings using Vertex AI and the Google Gen AI SDK."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the provider with application settings.

        Args:
            settings: Resolved application settings.
        """
        self._settings = settings
        self._client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )

    def embed_query(self, query: str) -> list[float]:
        """Generate an embedding vector for a user query.

        Args:
            query: User query text.

        Returns:
            A numeric embedding vector.
        """
        response = self._client.models.embed_content(
            model=self._settings.embedding_model_name,
            contents=query,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=self._settings.embedding_dimensions,
            ),
        )
        return response.embeddings[0].values
