# Product Embeddings Backfill Script

This script processes pending products in PostgreSQL, generates embeddings with Vertex AI, and stores them back in a `pgvector` column.

It is designed to backfill or refresh embeddings for product records whose `raw_text` has changed or whose embedding is missing.

## What it does

For each pending product, the script:

- Reads `raw_text` from PostgreSQL.
- Generates an embedding using Vertex AI.
- Converts the embedding to the `pgvector` format.
- Updates the product row with:
  - `embedding`
  - `embedding_model`
  - `embedded_at`
  - `embedding_text_hash`

## Flow

```text
PostgreSQL -> Pending rows -> Vertex AI embeddings -> pgvector update
```

## Requirements

- Python 3.11+
- PostgreSQL with `pgvector`
- Google Cloud project with Vertex AI enabled
- Python packages:
  - `psycopg2`
  - `google-genai`

## Environment variables

Set these before running the script:

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="your-location"
export EMBEDDING_MODEL_NAME="your-embedding-model"
export EMBEDDING_DIMENSIONS="your-embedding-dimensions"
export DB_HOST="your-db-host"
export DB_PORT="your-db-port"
export DB_NAME="your-db-name"
export DB_USER="your-db-user"
export DB_PASSWORD="your-db-password"
```

## Database assumptions

The script expects a table called `products` with at least these columns:

- `id`
- `raw_text`
- `embedding`
- `embedding_model`
- `embedded_at`
- `updated_at`
- `embedding_text_hash`

The `embedding` column should be compatible with `pgvector`.

## Run locally

```bash
python3 embed_products.py
```

## Run with a limit

Process only the first N pending products:

```bash
python3 embed_products.py --limit 100
```

## How it works

The script selects products that meet this condition:

- `raw_text` is not empty
- `embedding` is missing, or
- `embedded_at` is missing, or
- the embedding is older than `updated_at`

That means it can be used both for initial backfill and for refreshing outdated embeddings.

## Notes

- Each product is committed independently, so one failure does not stop the whole batch.
- A short sleep is added between requests to avoid overwhelming the embedding service.
- The text hash helps track whether the indexed content changed.
- The script uses `RETRIEVAL_DOCUMENT` as the embedding task type.

## Example output

```text
Productos pendientes: 42
[1/42] OK producto=101
[2/42] OK producto=102
[3/42] ERROR producto=103: ...
```

## Troubleshooting

If the script fails to connect to PostgreSQL, check:

- database host
- port
- user and password
- network access
- PostgreSQL is running

If Vertex AI fails, check:

- Google Cloud project
- location
- embedding model name
- credentials / authentication

## Related pieces

This script is meant to support a semantic search or RAG workflow by keeping product embeddings up to date in the database.