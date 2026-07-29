# Semantic Search API

This project exposes a FastAPI application for semantic product search and RAG-style chat over a cosmetics catalog.

The codebase follows a pragmatic hexagonal architecture with three main layers:

- **Controllers**: FastAPI endpoints and HTTP request/response mapping.
- **Services**: Application use cases and orchestration logic.
- **Repositories / Providers**: Infrastructure adapters for PostgreSQL and Vertex AI.

## Architecture

```text
HTTP -> Controller -> Service -> Ports -> Adapters
```

### Layers

- `app/domain`: core models and port contracts.
- `app/application`: DTOs and use-case services.
- `app/infrastructure`: configuration, database access, AI adapters, and web controllers.
- `app/main.py`: application wiring and FastAPI bootstrap.

## Project tree

```text
api/
  app/
    main.py
    domain/
      models/
        product.py
      ports/
        embedding_provider.py
        llm_provider.py
        product_repository.py
    application/
      dto/
        ask_dto.py
        search_dto.py
      services/
        rag_chat_service.py
        semantic_search_service.py
    infrastructure/
      config/
        settings.py
      database/
        connection.py
      repositories/
        postgres_product_repository.py
      ai/
        vertex_embedding_provider.py
        vertex_llm_provider.py
      web/
        controllers/
          ask_controller.py
          health_controller.py
          search_controller.py
  README.md
```

## Requirements

- Python 3.11+
- PostgreSQL with pgvector
- Google Cloud project with Vertex AI enabled

## Local setup

From the `api/` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn google-genai psycopg2-binary
```

## Environment variables

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="global"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="miin_poc"
export DB_USER="your-db-user"
export DB_PASSWORD="your-db-password"
export EMBEDDING_MODEL_NAME="gemini-embedding-001"
export GENERATION_MODEL_NAME="gemini-2.5-flash"
export EMBEDDING_DIMENSIONS="768"
export HNSW_EF_SEARCH="200"
export DEBUG_LLM="false"
```

## Run locally

From the `api/` folder, with the virtual environment activated:

```bash
python3 -m uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `POST /search`
- `POST /ask`

## Notes

- `/search` performs semantic retrieval only.
- `/ask` performs semantic retrieval first and then calls the LLM with the retrieved context.
- The application expects the backend dependencies to be installed inside the active virtual environment.
- The `app` package must be imported from inside the `api/` directory when running Uvicorn with this project layout.

## Troubleshooting

If you see `ModuleNotFoundError`, make sure:

- the virtual environment is activated,
- `fastapi`, `uvicorn`, `google-genai`, and `psycopg2-binary` are installed,
- you are running the command from `api/`,
- the environment variables are exported in the same terminal session.