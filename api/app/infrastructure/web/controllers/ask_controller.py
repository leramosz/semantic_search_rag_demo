"""HTTP controller exposing grounded chat endpoints."""

from fastapi import APIRouter, HTTPException

from app.application.dto.ask_dto import AskRequest, AskResponse, AskSourceResponse
from app.application.services.rag_chat_service import RagChatService


def build_ask_router(rag_chat_service: RagChatService) -> APIRouter:
    """Build the router for grounded chat endpoints.

    Args:
        rag_chat_service: Service that executes retrieval plus generation.

    Returns:
        A configured FastAPI router.
    """
    router = APIRouter(tags=["ask"])

    @router.post("/ask", response_model=AskResponse)
    def ask(request: AskRequest) -> AskResponse:
        """Answer a user question using semantic retrieval and an LLM.

        Args:
            request: HTTP payload containing the user query and top_k.

        Returns:
            A grounded chat answer plus the sources used.

        Raises:
            HTTPException: If the request contains an invalid query.
        """
        try:
            answer, results = rag_chat_service.ask(request.query, request.top_k)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

        return AskResponse(
            query=request.query.strip(),
            top_k=request.top_k,
            answer=answer,
            sources=[
                AskSourceResponse(
                    id=result.id,
                    name=result.name,
                    url=result.url,
                    similarity=result.similarity,
                )
                for result in results
            ],
        )

    return router
