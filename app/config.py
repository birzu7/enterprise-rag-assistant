from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", 500)
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", 50)
)

VECTOR_DB_PATH = os.getenv(
    "VECTOR_DB_PATH",
    "index"
)