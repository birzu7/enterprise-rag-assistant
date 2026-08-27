import json
from pathlib import Path

import faiss
import numpy as np

from app.embeddings import generate_embeddings
from app.load_documents import load_all_pdfs


def build_faiss_index(
    embedded_documents: list[dict],
) -> faiss.IndexFlatIP:
    """
    Build a FAISS index from normalized embedding vectors.
    """

    if not embedded_documents:
        raise ValueError(
            "No embedded documents were provided"
        )

    embedding_matrix = np.array(
        [
            document["embedding"]
            for document in embedded_documents
        ],
        dtype="float32",
    )

    embedding_dimension = embedding_matrix.shape[1]

    index = faiss.IndexFlatIP(
        embedding_dimension
    )

    index.add(
        embedding_matrix
    )

    return index


def save_faiss_index(
    index: faiss.Index,
    embedded_documents: list[dict],
    index_directory: str = "index",
) -> None:
    """
    Save the FAISS index and matching document metadata.
    """

    index_folder = Path(
        index_directory
    )

    index_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    faiss_path = (
        index_folder
        / "documents.faiss"
    )

    metadata_path = (
        index_folder
        / "metadata.json"
    )

    faiss.write_index(
        index,
        str(faiss_path),
    )

    metadata = []

    for document in embedded_documents:
        metadata_document = {
            key: value
            for key, value
            in document.items()
            if key != "embedding"
        }

        metadata.append(
            metadata_document
        )

    metadata_path.write_text(
        json.dumps(
            metadata,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Saved FAISS index to: "
        f"{faiss_path}"
    )

    print(
        f"Saved metadata to: "
        f"{metadata_path}"
    )


def load_faiss_index(
    index_directory: str = "index",
) -> tuple[
    faiss.Index,
    list[dict],
]:
    """
    Load the saved FAISS index and matching metadata.
    """

    index_folder = Path(
        index_directory
    )

    faiss_path = (
        index_folder
        / "documents.faiss"
    )

    metadata_path = (
        index_folder
        / "metadata.json"
    )

    if not faiss_path.exists():
        raise FileNotFoundError(
            f"FAISS index not found: "
            f"{faiss_path}"
        )

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Metadata file not found: "
            f"{metadata_path}"
        )

    index = faiss.read_index(
        str(faiss_path)
    )

    metadata = json.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )

    if index.ntotal != len(metadata):
        raise ValueError(
            "FAISS vector count does not "
            "match metadata count"
        )

    return index, metadata


def rebuild_vector_index(
    index_directory: str = "index",
) -> dict:
    """
    Run the complete document indexing pipeline.

    Steps:
    1. Load and preprocess PDFs.
    2. Chunk the documents.
    3. Generate embeddings.
    4. Build the FAISS index.
    5. Save the FAISS index and metadata.
    6. Reload the saved index for verification.
    """

    print(
        "Starting vector index rebuild..."
    )

    # Step 1:
    # Load PDFs.
    # load_all_pdfs() already performs the
    # preprocessing and chunking pipeline.
    documents = load_all_pdfs()

    print(
        f"Loaded {len(documents)} "
        f"document chunk(s)."
    )

    # Step 2:
    # Generate embeddings.
    embedded_documents = (
        generate_embeddings(
            documents
        )
    )

    print(
        f"Generated embeddings for "
        f"{len(embedded_documents)} "
        f"chunk(s)."
    )

    # Step 3:
    # Build FAISS index.
    faiss_index = build_faiss_index(
        embedded_documents
    )

    print(
        f"FAISS index contains "
        f"{faiss_index.ntotal} vectors."
    )

    print(
        f"Embedding dimension: "
        f"{faiss_index.d}"
    )

    # Step 4:
    # Save FAISS and metadata.
    save_faiss_index(
        index=faiss_index,
        embedded_documents=(
            embedded_documents
        ),
        index_directory=(
            index_directory
        ),
    )

    # Step 5:
    # Verify the saved files.
    loaded_index, loaded_metadata = (
        load_faiss_index(
            index_directory=(
                index_directory
            )
        )
    )

    print(
        f"Verified FAISS index with "
        f"{loaded_index.ntotal} vectors."
    )

    print(
        f"Verified "
        f"{len(loaded_metadata)} "
        f"metadata records."
    )

    print(
        "Vector index rebuild completed."
    )

    # Return a summary.
    # This becomes useful later for Airflow.
    return {
        "document_chunks": (
            len(documents)
        ),
        "embedded_chunks": (
            len(embedded_documents)
        ),
        "vectors": (
            loaded_index.ntotal
        ),
        "embedding_dimension": (
            loaded_index.d
        ),
        "metadata_records": (
            len(loaded_metadata)
        ),
    }


if __name__ == "__main__":
    result = rebuild_vector_index()

    print("-" * 50)
    print("INDEX REBUILD SUMMARY")

    print(
        f"Document chunks: "
        f"{result['document_chunks']}"
    )

    print(
        f"Embedded chunks: "
        f"{result['embedded_chunks']}"
    )

    print(
        f"Vectors: "
        f"{result['vectors']}"
    )

    print(
        f"Embedding dimension: "
        f"{result['embedding_dimension']}"
    )

    print(
        f"Metadata records: "
        f"{result['metadata_records']}"
    )