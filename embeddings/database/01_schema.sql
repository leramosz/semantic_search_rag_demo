CREATE TABLE IF NOT EXISTS public.products
(
    id bigint NOT NULL DEFAULT nextval('products_id_seq'::regclass),
    url text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default",
    brand text COLLATE pg_catalog."default",
    price_current numeric(10,2),
    short_description text COLLATE pg_catalog."default",
    raw_text text COLLATE pg_catalog."default",
    created_at timestamp with time zone DEFAULT now(),
    benefits_text text COLLATE pg_catalog."default",
    ingredients_text text COLLATE pg_catalog."default",
    updated_at timestamp with time zone DEFAULT now(),
    product_type text COLLATE pg_catalog."default",
    embedding vector(768),
    embedding_model text COLLATE pg_catalog."default",
    embedded_at timestamp with time zone,
    embedding_text_hash text COLLATE pg_catalog."default",
    CONSTRAINT products_pkey PRIMARY KEY (id),
    CONSTRAINT products_url_key UNIQUE (url)
);

TABLESPACE pg_default;