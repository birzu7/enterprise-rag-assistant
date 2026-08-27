from app.retrieval import search_documents
from app.vector_store import load_faiss_index


EVALUATION_SET = [
    {
        "question": "What are CirQX's revenue streams?",
        "expected_source": "Doc1_CirQX Business Blueprint.pdf",
        "expected_keywords": [
            "Revenue Streams",
            "Subscription",
        ],
    },
    {
        "question": "How does CirQX forecast demand?",
        "expected_source": "Doc2_CirQX flowchart.pdf",
        "expected_keywords": [
            "forecast",
            "demand",
        ],
    },
    {
        "question": "How does CirQX support recycling?",
        "expected_source": "Doc1_CirQX Business Blueprint.pdf",
        "expected_keywords": [
            "recycling",
        ],
    },
]


def evaluate_retrieval(
    top_k: int = 5,
) -> None:
    """
    Evaluate whether retrieval returns the expected source
    and relevant keywords.
    """

    index, metadata = load_faiss_index()

    total_questions = len(EVALUATION_SET)

    source_hits = 0
    keyword_hits = 0

    for item in EVALUATION_SET:
        question = item["question"]
        expected_source = item["expected_source"]
        expected_keywords = item["expected_keywords"]

        results = search_documents(
            question=question,
            index=index,
            metadata=metadata,
            top_k=top_k,
        )

        retrieved_sources = [
            result["source_name"]
            for result in results
        ]

        source_found = (
            expected_source in retrieved_sources
        )

        combined_text = " ".join(
            result["text"]
            for result in results
        ).lower()

        keyword_found = all(
            keyword.lower() in combined_text
            for keyword in expected_keywords
        )

        if source_found:
            source_hits += 1

        if keyword_found:
            keyword_hits += 1

        print("=" * 60)
        print(f"Question: {question}")
        print(f"Expected source: {expected_source}")

        print(
            f"Source result: "
            f"{'PASS' if source_found else 'FAIL'}"
        )

        print(
            f"Keyword result: "
            f"{'PASS' if keyword_found else 'FAIL'}"
        )

        print("Top retrieved chunks:")

        for rank, result in enumerate(
            results,
            start=1,
        ):
            print(
                f"{rank}. "
                f"{result['source_name']} "
                f"| Chunk {result['chunk_index']} "
                f"| Score {result['score']:.3f}"
            )

    source_hit_rate = (
        source_hits / total_questions
    )

    keyword_hit_rate = (
        keyword_hits / total_questions
    )

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print(
        f"Source Hit Rate: "
        f"{source_hits}/{total_questions} "
        f"({source_hit_rate:.0%})"
    )

    print(
        f"Keyword Hit Rate: "
        f"{keyword_hits}/{total_questions} "
        f"({keyword_hit_rate:.0%})"
    )


if __name__ == "__main__":
    evaluate_retrieval(
        top_k=5,
    )