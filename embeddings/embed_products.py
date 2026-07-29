import argparse
import hashlib
import os
import time

import psycopg2
from google import genai
from google.genai import types


# PostgreSQL connection settings loaded from environment variables.
DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ["DB_PORT"]),
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
}

# Vertex AI / embeddings configuration.
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
MODEL_NAME = os.environ["EMBEDDING_MODEL_NAME"]
DIMENSIONS = int(os.environ["EMBEDDING_DIMENSIONS"])

# Embedding task type: document retrieval.
TASK_TYPE = "RETRIEVAL_DOCUMENT"

# Small pause between requests to avoid overloading the service.
SLEEP_SECONDS = 0.05


def parse_args():
    # Parse command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only N pending records.",
    )
    return parser.parse_args()


def text_hash(text: str) -> str:
    # Generate a stable hash for the normalized text.
    normalized = text.strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def vector_to_pg(values: list[float]) -> str:
    # Convert a float list to the format expected by pgvector.
    return "[" + ",".join(str(v) for v in values) + "]"


def get_pending_products(conn, limit=None):
    # Fetch products that still need an embedding or have an outdated one.
    sql = """
        SELECT id, raw_text
        FROM products
        WHERE raw_text IS NOT NULL
          AND btrim(raw_text) <> ''
          AND (
              embedding IS NULL
              OR embedded_at IS NULL
              OR embedded_at < updated_at
          )
        ORDER BY id
    """
    params = []

    if limit is not None:
        sql += " LIMIT %s"
        params.append(limit)

    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def main():
    # Read CLI arguments.
    args = parse_args()

    # Create the Vertex AI client for embedding generation.
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
    )

    # Open the PostgreSQL connection.
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False

    try:
        rows = get_pending_products(conn, limit=args.limit)
        total = len(rows)
        print(f"Pending products: {total}")

        if total == 0:
            print("No pending products.")
            return

        for i, (product_id, raw_text) in enumerate(rows, start=1):
            try:
                # Generate an embedding for the product text.
                response = client.models.embed_content(
                    model=MODEL_NAME,
                    contents=raw_text,
                    config=types.EmbedContentConfig(
                        task_type=TASK_TYPE,
                        output_dimensionality=DIMENSIONS,
                    ),
                )

                embedding = response.embeddings[0].values
                content_hash = text_hash(raw_text)

                # Store the vector, model name, timestamp, and text hash in the database.
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE products
                        SET embedding = %s::vector,
                            embedding_model = %s,
                            embedded_at = NOW(),
                            embedding_text_hash = %s
                        WHERE id = %s;
                    """, (
                        vector_to_pg(embedding),
                        MODEL_NAME,
                        content_hash,
                        product_id,
                    ))

                # Commit this product independently to keep the process incremental.
                conn.commit()
                print(f"[{i}/{total}] OK product={product_id}")

            except Exception as e:
                # Roll back only this product if something fails.
                conn.rollback()
                print(f"[{i}/{total}] ERROR product={product_id}: {e}")

            # Short pause between model calls.
            time.sleep(SLEEP_SECONDS)

    finally:
        conn.close()


if __name__ == "__main__":
    main()