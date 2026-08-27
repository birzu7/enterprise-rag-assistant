from sentence_transformers import SentenceTransformer

from app.load_documents import load_all_pdfs
from app.config import EMBEDDING_MODEL


embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


def generate_embedding(text: str):
    """
    Generate one normalized embedding vector.
    """

    return embedding_model.encode(
        text,
        normalize_embeddings=True,
    )


def generate_embeddings(documents: list[dict]) -> list[dict]:
    """
    Generate embeddings for all document chunks in one batch.
    """

    if not documents:
        return []

    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    embedded_documents = []

    for document, embedding in zip(
        documents,
        embeddings,
    ):
        embedded_document = document.copy()
        embedded_document["embedding"] = embedding

        embedded_documents.append(
            embedded_document
        )

    return embedded_documents


if __name__ == "__main__":

    documents = load_all_pdfs()

    embedded_documents = generate_embeddings(
        documents
    )

    print(
        f"Embedded {len(embedded_documents)} chunks."
    )

    print("-" * 50)

    first_document = embedded_documents[0]

    print(
        f"File: {first_document['source_name']}"
    )

    print(
        f"Chunk Index: {first_document['chunk_index']}"
    )

    print(
        f"Embedding Shape: "
        f"{first_document['embedding'].shape}"
    )

    print(
        f"First 10 Values:"
    )

    print(
        first_document["embedding"][:10]
    )