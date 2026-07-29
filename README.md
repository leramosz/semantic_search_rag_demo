# Semantic Search RAG Demo

This repository contains a small proof of concept for a semantic search and RAG-style experience built around a product catalog.

The project is split into three main areas:

- **api**: backend logic for searching products and returning answers.
- **embeddings**: scripts and utilities for generating and refreshing product embeddings in PostgreSQL.
- **web**: static frontend for testing the demo through a chat-style interface.

Each folder includes its own README with the implementation details for that specific part of the system.

## Repository structure

```text
semantic_search_rag_demo/
├── api/
│   └── README.md
├── embeddings/
│   └── README.md
├── web/
│   └── README.md
└── README.md
```

## What you will find in each folder

### `api/`

Backend service for semantic search and RAG-style responses.

You will find:

- the HTTP API,
- the search logic,
- the grounding / LLM integration,
- the configuration needed to connect to PostgreSQL and Vertex AI.

See `api/README.md` for setup instructions, environment variables, and endpoints.

### `embeddings/`

Batch scripts used to generate and refresh embeddings for product data.

You will find:

- the embedding backfill script,
- PostgreSQL update logic,
- Vertex AI embedding generation,
- hash and sync logic for keeping vectors up to date.

See `embeddings/README.md` for execution details and required environment variables.

### `web/`

Static frontend used to interact with the demo from the browser.

You will find:

- the chat UI,
- the theme switch,
- the endpoint configuration,
- the browser-side logic to call the backend API.

See `web/README.md` for details.

## Requirements

- Python 3.11+
- PostgreSQL with `pgvector`
- Google Cloud project with Vertex AI enabled

## High-level flow

```text
Catalog data -> Embeddings -> PostgreSQL / pgvector -> Semantic search -> Grounded answer -> Web UI
```

## Notes

- This repository is meant as a POC and learning exercise.
- The code is organized so each part of the system can evolve independently.
- The detailed implementation of each module lives in the README inside each folder.