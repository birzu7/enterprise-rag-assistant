from pathlib import Path

from pypdf import PdfReader

from app.chunking import chunk_document
from app.preprocess import preprocess_document


def load_pdf(file_path: Path) -> dict:
    """
    Load one PDF, extract its text, preserve metadata,
    and preprocess the document.
    """

    reader = PdfReader(file_path)

    page_texts = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            page_texts.append(text)

    full_text = "\n".join(page_texts)

    if not full_text.strip():
        print(
            f"Warning: No extractable text found in "
            f"{file_path.name}"
        )

    document = {
        "text": full_text,
        "source_type": "pdf",
        "source_name": file_path.name,
        "source_path": str(file_path),
        "page_count": len(reader.pages),
    }

    return preprocess_document(document)


def load_all_pdfs(
    pdf_directory: str = "data/raw/pdf",
) -> list[dict]:
    """
    Load every PDF in a folder and return document chunks.
    """

    pdf_folder = Path(pdf_directory)

    if not pdf_folder.exists():
        raise FileNotFoundError(
            f"PDF directory not found: {pdf_folder}"
        )

    chunked_documents = []

    for pdf_file in sorted(pdf_folder.glob("*.pdf")):
        try:
            document = load_pdf(pdf_file)

            document_chunks = chunk_document(
                document=document,
                chunk_size=500,
                chunk_overlap=50,
            )

            chunked_documents.extend(document_chunks)

        except Exception as error:
            print(
                f"Warning: Could not load {pdf_file.name}"
            )
            print(f"Reason: {error}")

    return chunked_documents


if __name__ == "__main__":
    documents = load_all_pdfs()

    print(
        f"Loaded {len(documents)} document chunk(s)."
    )

    for document in documents:
        print("-" * 50)
        print(f"File: {document['source_name']}")
        print(f"Pages: {document['page_count']}")
        print(
            f"Chunk Index: {document['chunk_index']}"
        )
        print(
            f"Chunk Characters: "
            f"{len(document['text'])}"
        )
        print(
            f"Preview: {document['text'][:300]}"
        )