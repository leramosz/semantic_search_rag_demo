# Database scripts

This folder contains the SQL scripts used to create the base product table, load catalog data, enable pgvector, and create the vector index.

The catalog data is intentionally separated from the embedding pipeline.

## Files

- `01_schema.sql`: creates `public.products`.
- `02_seed.sql`: inserts catalog data without embeddings.
- `03_pgvector.sql`: enables the `vector` extension.
- `04_vector_index.sql`: creates the HNSW index for semantic search.

## Execution order

```text
01_schema.sql
02_seed.sql
03_pgvector.sql
04_vector_index.sql
```

## Notes

- The embedding-related fields stay empty until the embedding pipeline runs.
- The vector index should be created after the data is loaded.
- The `url` column is unique.