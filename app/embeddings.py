from app.load_documents import load_all_pdfs


def generate_embedding(text: str):
    """
    Temporary test embedding.

    Returns a fake 384-dimensional vector so we can
    determine whether sentence-transformers is causing
    the Render crash.
    """

    return [0.0] * 384


def generate_embeddings(
    documents: list[dict],
) -> list[dict]:
    """
    Temporary batch embedding generator.
    """

    if not documents:
        return []

    embedded_documents = []

    for document in documents:

        embedded_document = document.copy()

        embedded_document[
            "embedding"
        ] = [0.0] * 384

        embedded_documents.append(
            embedded_document
        )

    return embedded_documents


if __name__ == "__main__":

    documents = load_all_pdfs()

    embedded_documents = (
        generate_embeddings(
            documents
        )
    )

    print(
        f"Embedded {len(embedded_documents)} chunks."
    )

    print("-" * 50)

    first_document = (
        embedded_documents[0]
    )

    print(
        f"File: "
        f"{first_document['source_name']}"
    )

    print(
        f"Chunk Index: "
        f"{first_document['chunk_index']}"
    )

    print(
        f"Embedding Length: "
        f"{len(first_document['embedding'])}"
    )

    print("First 10 Values:")

    print(
        first_document[
            "embedding"
        ][:10]
    )