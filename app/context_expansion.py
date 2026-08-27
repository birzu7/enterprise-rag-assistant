def expand_with_neighbors(
    retrieved_documents: list[dict],
    metadata: list[dict],
    neighbor_window: int = 1,
    max_seed_documents: int = 2,
    max_context_chunks: int = 6,
) -> list[dict]:
    """
    Expand only the strongest retrieved chunks with nearby chunks.

    Example:
    If FAISS returns chunks 9 and 15 as the best matches,
    include neighbors around those chunks, while removing duplicates
    and limiting the final context size.
    """

    if neighbor_window < 0:
        raise ValueError(
            "neighbor_window cannot be negative"
        )

    if max_seed_documents <= 0:
        raise ValueError(
            "max_seed_documents must be greater than 0"
        )

    if max_context_chunks <= 0:
        raise ValueError(
            "max_context_chunks must be greater than 0"
        )

        # Select strong seeds while encouraging source diversity.
    seed_documents = []
    seen_sources = set()

    # First pass: choose the best result from different sources.
    for document in retrieved_documents:
        source_name = document["source_name"]

        if source_name not in seen_sources:
            seed_documents.append(document)
            seen_sources.add(source_name)

        if len(seed_documents) >= max_seed_documents:
            break

    # Second pass: if we still need more seeds,
    # fill them with the next strongest results.
    if len(seed_documents) < max_seed_documents:
        for document in retrieved_documents:
            if document in seed_documents:
                continue

            seed_documents.append(document)

            if len(seed_documents) >= max_seed_documents:
                break

    expanded_documents = []
    seen = set()

    for seed_document in seed_documents:
        source_name = seed_document[
            "source_name"
        ]

        chunk_index = seed_document[
            "chunk_index"
        ]

        start_index = max(
            0,
            chunk_index - neighbor_window,
        )

        end_index = (
            chunk_index + neighbor_window
        )

        for metadata_document in metadata:
            same_source = (
                metadata_document["source_name"]
                == source_name
            )

            nearby_chunk = (
                start_index
                <= metadata_document["chunk_index"]
                <= end_index
            )

            if not (
                same_source
                and nearby_chunk
            ):
                continue

            unique_key = (
                metadata_document["source_name"],
                metadata_document["chunk_index"],
            )

            if unique_key in seen:
                continue

            expanded_document = (
                metadata_document.copy()
            )

            # Preserve the FAISS score only for
            # the original retrieved chunk.
            if (
                metadata_document["chunk_index"]
                == chunk_index
            ):
                expanded_document[
                    "score"
                ] = seed_document.get(
                    "score"
                )

                expanded_document[
                    "retrieval_type"
                ] = "semantic_match"

            else:
                expanded_document[
                    "retrieval_type"
                ] = "neighbor"

            expanded_documents.append(
                expanded_document
            )

            seen.add(unique_key)

    expanded_documents.sort(
        key=lambda document: (
            document["source_name"],
            document["chunk_index"],
        )
    )

    return expanded_documents[
        :max_context_chunks
    ]


if __name__ == "__main__":
    metadata = [
        {
            "source_name": "Doc1.pdf",
            "chunk_index": 8,
            "text": "Previous section",
        },
        {
            "source_name": "Doc1.pdf",
            "chunk_index": 9,
            "text": "Revenue Streams",
        },
        {
            "source_name": "Doc1.pdf",
            "chunk_index": 10,
            "text": "More revenue details",
        },
        {
            "source_name": "Doc2.pdf",
            "chunk_index": 4,
            "text": "Inventory planning",
        },
        {
            "source_name": "Doc2.pdf",
            "chunk_index": 5,
            "text": "Business value",
        },
        {
            "source_name": "Doc2.pdf",
            "chunk_index": 6,
            "text": "Forecasting",
        },
    ]

    retrieved_documents = [
        {
            "source_name": "Doc1.pdf",
            "chunk_index": 9,
            "text": "Revenue Streams",
            "score": 0.82,
        },
        {
            "source_name": "Doc2.pdf",
            "chunk_index": 5,
            "text": "Business value",
            "score": 0.70,
        },
        {
            "source_name": "Doc2.pdf",
            "chunk_index": 6,
            "text": "Forecasting",
            "score": 0.55,
        },
    ]

    expanded = expand_with_neighbors(
        retrieved_documents=(
            retrieved_documents
        ),
        metadata=metadata,
        neighbor_window=1,
        max_seed_documents=2,
        max_context_chunks=6,
    )

    print(
        f"Expanded to "
        f"{len(expanded)} chunks."
    )

    for document in expanded:
        print("-" * 40)
        print(
            f"Source: "
            f"{document['source_name']}"
        )
        print(
            f"Chunk: "
            f"{document['chunk_index']}"
        )
        print(
            f"Type: "
            f"{document['retrieval_type']}"
        )

        if document.get("score") is not None:
            print(
                f"Score: "
                f"{document['score']:.3f}"
            )

        print(document["text"])