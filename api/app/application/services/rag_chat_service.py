"""Application service responsible for grounded chat generation."""

from app.domain.models.product import ProductSearchHit
from app.domain.ports.llm_provider import LlmProviderPort
from app.application.services.semantic_search_service import SemanticSearchService


class RagChatService:
    """Execute RAG chat use cases.

    This service first performs semantic retrieval and then delegates answer
    generation to an LLM provider using the retrieved products as context.
    """

    def __init__(self, search_service: SemanticSearchService, llm_provider: LlmProviderPort) -> None:
        """Initialize the service with its dependencies.

        Args:
            search_service: Semantic retrieval use case service.
            llm_provider: LLM adapter used to generate grounded answers.
        """
        self._search_service = search_service
        self._llm_provider = llm_provider

    def ask(self, query: str, top_k: int) -> tuple[str, list[ProductSearchHit]]:
        """Answer a user question using semantic retrieval plus generation.

        Args:
            query: User question.
            top_k: Maximum number of retrieved products.

        Returns:
            A tuple containing the generated answer and the search hits.
        """
        results = self._search_service.search(query, top_k)
        if not results:
            return (
                "No relevant products were found to answer the question with sufficient confidence.",
                [],
            )

        answer = self._llm_provider.answer_with_context(query, results)
        if not answer:
            answer = "Relevant products were found, but the model could not generate a useful answer."

        return answer, results
