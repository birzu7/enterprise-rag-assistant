import faiss
import numpy as np

from app.embeddings import generate_embedding
from app.vector_store import load_faiss_index


def search_documents(
    question: str,
    index: faiss.Index,
    metadata: list[dict],
    top_k: int = 10,
) -> list[dict]:
    """
    Search FAISS for the document chunks most similar
    to the user's question.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty")

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    if not metadata:
        return []

    top_k = min(top_k, index.ntotal)

    question_embedding = generate_embedding(
        question
    )

    question_embedding = np.array(
        [question_embedding],
        dtype="float32",
    )

    scores, indices = index.search(
        question_embedding,
        top_k,
    )

    results = []

    for score, index_id in zip(
        scores[0],
        indices[0],
    ):
        if index_id == -1:
            continue

        result = metadata[index_id].copy()

        result["score"] = float(score)
        result["vector_id"] = int(index_id)

        results.append(result)

    return results


if __name__ == "__main__":
    index, metadata = load_faiss_index()

    question = (
        "What subscription fees, marketplace commissions, "
        "recycling commissions, and brand partnerships "
        "generate revenue for CirQX?"
    )

    results = search_documents(
        question=question,
        index=index,
        metadata=metadata,
        top_k=10,
    )

    print(f"Question: {question}")
    print("=" * 60)

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print(f"Rank: {rank}")
        print(f"Score: {result['score']:.3f}")
        print(f"Vector ID: {result['vector_id']}")
        print(f"File: {result['source_name']}")
        print(f"Chunk: {result['chunk_index']}")
        print(result["text"])
        print("=" * 60)