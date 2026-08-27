from app.context_expansion import expand_with_neighbors
from app.llm import generate_answer
from app.prompt_builder import build_prompt
from app.retrieval import search_documents
from app.vector_store import load_faiss_index
import time

#from app.mlflow_tracking import track_rag_run


def answer_question(
    question: str,
    top_k: int = 5,
) -> dict:
    """
    Run the complete RAG pipeline.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty")
    start_time = time.perf_counter()

    index, metadata = load_faiss_index()

    retrieved_documents = search_documents(
        question=question,
        index=index,
        metadata=metadata,
        top_k=top_k,
    )

    if not retrieved_documents:
        return {
            "question": question,
            "answer": (
                "I could not find relevant information "
                "in the provided documents."
            ),
            "sources": [],
        }

    expanded_documents = expand_with_neighbors(
        retrieved_documents=retrieved_documents,
        metadata=metadata,
        neighbor_window=1,
        max_seed_documents=2,
        max_context_chunks=6,
    )

    prompt = build_prompt(
        question=question,
        retrieved_documents=expanded_documents,
    )

    answer = generate_answer(prompt)

    response_time = time.perf_counter() - start_time

    #track_rag_run(
    #question=question,
    #answer=answer,
    sources=expanded_documents,
    #response_time=response_time,
    #top_k=top_k,
#)

    return {
        "question": question,
        "answer": answer,
        "sources": expanded_documents,
    }


if __name__ == "__main__":
    question = "What are CirQX's revenue streams?"

    result = answer_question(
        question=question,
        top_k=5,
    )

    print("QUESTION:")
    print(result["question"])

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print("-" * 50)
        print(f"File: {source['source_name']}")
        print(f"Chunk: {source['chunk_index']}")
        print(
            f"Type: "
            f"{source.get('retrieval_type', 'unknown')}"
        )

        if source.get("score") is not None:
            print(f"Score: {source['score']:.3f}")

        print("TEXT:")
        print(source["text"])