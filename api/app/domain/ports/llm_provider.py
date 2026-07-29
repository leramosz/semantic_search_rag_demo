"""LLM provider port definitions."""

from typing import Protocol

from app.domain.models.product import ProductSearchHit


class LlmProviderPort(Protocol):
    """Define the contract for grounded chat generation."""

    def answer_with_context(self, user_query: str, results: list[ProductSearchHit]) -> str:
        """Generate a chat-style answer using retrieved context.

        Args:
            user_query: Original user question.
            results: Products retrieved by semantic search.

        Returns:
            A grounded conversational answer.
        """
