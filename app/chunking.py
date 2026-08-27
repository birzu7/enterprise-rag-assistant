import re

from typing import List

from app.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[str]:
    """
    Split text into overlapping character-based chunks
    without cutting words.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative"
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0

    while start < len(text):

        end = min(
            start + chunk_size,
            len(text),
        )

        if end < len(text):

            last_space = text.rfind(
                " ",
                start,
                end,
            )

            if last_space > start:
                end = last_space

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        next_start = max(
            0,
            end - chunk_overlap,
        )

        next_space = text.find(
            " ",
            next_start,
            end,
        )

        if next_space != -1:
            next_start = next_space + 1

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


def chunk_text_by_paragraphs(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[str]:
    """
    Group paragraphs into focused chunks while
    attempting to preserve paragraph boundaries.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative"
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(
            r"\n\s*\n",
            text,
        )
        if paragraph.strip()
    ]

    chunks = []

    current_paragraphs = []

    current_length = 0

    for paragraph in paragraphs:

        paragraph_length = len(paragraph)

        if paragraph_length > chunk_size:

            if current_paragraphs:

                chunks.append(
                    "\n\n".join(
                        current_paragraphs
                    )
                )

                current_paragraphs = []

                current_length = 0

            large_paragraph_chunks = chunk_text(
                text=paragraph,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            chunks.extend(
                large_paragraph_chunks
            )

            continue

        separator_length = (
            2 if current_paragraphs else 0
        )

        proposed_length = (
            current_length
            + separator_length
            + paragraph_length
        )

        if proposed_length <= chunk_size:

            current_paragraphs.append(
                paragraph
            )

            current_length = proposed_length

            continue

        if current_paragraphs:

            completed_chunk = "\n\n".join(
                current_paragraphs
            )

            chunks.append(
                completed_chunk
            )

        overlap_paragraphs = []

        overlap_length = 0

        for previous_paragraph in reversed(
            current_paragraphs
        ):

            additional_length = (
                len(previous_paragraph)
                + (
                    2
                    if overlap_paragraphs
                    else 0
                )
            )

            if (
                overlap_length
                + additional_length
                > chunk_overlap
            ):
                break

            overlap_paragraphs.insert(
                0,
                previous_paragraph,
            )

            overlap_length += (
                additional_length
            )

        current_paragraphs = (
            overlap_paragraphs
            + [paragraph]
        )

        current_length = len(
            "\n\n".join(
                current_paragraphs
            )
        )

    if current_paragraphs:

        chunks.append(
            "\n\n".join(
                current_paragraphs
            )
        )

    return chunks


def chunk_document(
    document: dict,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[dict]:
    """
    Split one document into paragraph-aware chunks
    while preserving its metadata.
    """

    text_chunks = chunk_text_by_paragraphs(
        text=document["text"],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunked_documents = []

    for chunk_index, chunk_text_value in enumerate(
        text_chunks
    ):

        chunk_document_data = (
            document.copy()
        )

        chunk_document_data["text"] = (
            chunk_text_value
        )

        chunk_document_data[
            "chunk_index"
        ] = chunk_index

        chunked_documents.append(
            chunk_document_data
        )

    return chunked_documents


if __name__ == "__main__":

    sample_document = {
        "text": """
Artificial Intelligence is transforming businesses.

Companies use AI to automate repetitive tasks,
improve forecasting, and support better decisions.

Retailers can use machine learning to predict demand,
reduce stockouts, and optimize inventory.

AI systems also help companies analyze large amounts
of business data more quickly.
        """,
        "source_type": "test",
        "source_name": "sample_document.txt",
        "source_path": "test/sample_document.txt",
        "page_count": 1,
    }

    chunks = chunk_document(
        document=sample_document,
        chunk_size=180,
        chunk_overlap=50,
    )

    print(
        f"Total Chunks: {len(chunks)}"
    )

    for chunk in chunks:

        print("-" * 50)

        print(
            f"Source: "
            f"{chunk['source_name']}"
        )

        print(
            f"Chunk Index: "
            f"{chunk['chunk_index']}"
        )

        print(
            f"Characters: "
            f"{len(chunk['text'])}"
        )

        print(chunk["text"])