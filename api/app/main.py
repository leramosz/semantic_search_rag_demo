"""Application bootstrap and dependency wiring for the MIIN API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.services.rag_chat_service import RagChatService
from app.application.services.semantic_search_service import SemanticSearchService
from app.infrastructure.ai.vertex_embedding_provider import VertexEmbeddingProvider
from app.infrastructure.ai.vertex_llm_provider import VertexLlmProvider
from app.infrastructure.config.settings import Settings
from app.infrastructure.database.connection import PostgresConnectionFactory
from app.infrastructure.repositories.postgres_product_repository import PostgresProductRepository
from app.infrastructure.web.controllers.ask_controller import build_ask_router
from app.infrastructure.web.controllers.health_controller import router as health_router
from app.infrastructure.web.controllers.search_controller import build_search_router


"""Instantiate infrastructure settings from environment variables."""
settings = Settings()

"""Create the shared PostgreSQL connection factory."""
connection_factory = PostgresConnectionFactory(settings)

"""Create repository and AI adapters."""
product_repository = PostgresProductRepository(connection_factory)
embedding_provider = VertexEmbeddingProvider(settings)
llm_provider = VertexLlmProvider(settings)

"""Create application services."""
semantic_search_service = SemanticSearchService(
    embedding_provider=embedding_provider,
    product_repository=product_repository,
    ef_search=settings.hnsw_ef_search,
)
rag_chat_service = RagChatService(
    search_service=semantic_search_service,
    llm_provider=llm_provider,
)

"""Create the FastAPI application."""
app = FastAPI(title="MIIN Semantic Search API")
app.include_router(health_router)
app.include_router(build_search_router(semantic_search_service))
app.include_router(build_ask_router(rag_chat_service))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)