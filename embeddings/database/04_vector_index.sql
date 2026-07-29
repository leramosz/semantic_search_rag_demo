CREATE INDEX IF NOT EXISTS products_embedding_hnsw_idx
    ON public.products USING hnsw
    (embedding vector_cosine_ops)
    
TABLESPACE pg_default;