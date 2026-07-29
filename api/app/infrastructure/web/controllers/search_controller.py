"""HTTP controller exposing semantic search endpoints."""

from fastapi import APIRouter, HTTPException

from app.application.dto.search_dto import SearchRequest, SearchResponse, SearchResultResponse
from app.application.services.semantic_search_service import SemanticSearchService


def build_search_router(search_service: SemanticSearchService) -> APIRouter:
    """Build the router for semantic search endpoints.

    Args:
        search_service: Service that executes semantic search.

    Returns:
        A configured FastAPI router.
    """
    router = APIRouter(tags=["search"])

    @router.post("/search", response_model=SearchResponse)
    def search(request: SearchRequest) -> SearchResponse:
        """Execute semantic product search.

        Args:
            request: HTTP payload containing the user query and top_k.

        Returns:
            A semantic search response with ranked products.

        Raises:
            HTTPException: If the request contains an invalid query.
        """
        try:
            results = search_service.search(request.query, request.top_k)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

        return SearchResponse(
            query=request.query.strip(),
            top_k=request.top_k,
            results=[
                SearchResultResponse(
                    id=result.id,
                    name=result.name,
                    short_description=result.short_description,
                    url=result.url,
                    raw_text=result.raw_text,
                    similarity=result.similarity,
                )
                for result in results
            ],
        )

    return router
