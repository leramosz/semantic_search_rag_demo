# Semantic Search RAG Demo

A proof-of-concept demo for semantic product search and RAG-style chat over a cosmetics catalog.

The project combines a FastAPI backend, a PostgreSQL vector store, Google Vertex AI embeddings, and a static chat UI served with Python's built-in HTTP server.

## Live structure

This repository is organized into three main parts:

- **api**: FastAPI backend with semantic search and RAG endpoints.
- **embeddings**: scripts to generate and refresh product embeddings in PostgreSQL.
- **web**: static frontend chat UI for testing the demo in the browser.

Each folder includes its own README with the implementation details for that specific part.

## Architecture

```text
Web UI -> FastAPI API -> PostgreSQL / pgvector -> Vertex AI
```

## What this demo shows

- Semantic retrieval over product text.
- RAG-style answers grounded in retrieved catalog context.
- A clean, responsive chat interface.
- A separate embedding backfill pipeline for keeping vectors up to date.

## Project tree

```text
semantic_search_rag_demo/
├── api/
│   ├── app/
│   └── README.md
├── embeddings/
│   └── README.md
├── web/
│   └── README.md
└── README.md
```

## Tech stack

- Python 3.11+
- FastAPI
- Uvicorn
- PostgreSQL
- pgvector
- Google Vertex AI
- HTML, CSS, and vanilla JavaScript

## Requirements

- Python installed locally.
- PostgreSQL with `pgvector` enabled.
- Google Cloud project with Vertex AI enabled.
- Environment variables configured for the API and embeddings scripts.

## Run the API

From the `api/` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn google-genai psycopg2-binary
python3 -m uvicorn app.main:app --reload
```

## Run the web UI

From the `web/` folder:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

## Environment variables

The API and embeddings scripts expect variables like:

```bash
GOOGLE_CLOUD_PROJECT
GOOGLE_CLOUD_LOCATION
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
EMBEDDING_MODEL_NAME
GENERATION_MODEL_NAME
EMBEDDING_DIMENSIONS
HNSW_EF_SEARCH
DEBUG_LLM
```

See the README inside each folder for the exact values and usage.

## Notes

- The repository is intentionally split by responsibility to keep the code easy to navigate.
- The API handles search and generation.
- The embeddings folder handles indexing jobs.
- The web folder is only the frontend demo.
- The root README is a summary; deeper setup details live in each subfolder README.

## Screenshots

Add a screenshot or GIF here to show the UI and make the repo more attractive on GitHub.
