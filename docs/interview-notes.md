# Enterprise RAG Assistant Interview Notes

## 30-Second Project Summary

Enterprise RAG Assistant is an end-to-end Retrieval-Augmented Generation system that enables users to ask natural language questions over enterprise documents.

The system ingests PDFs, preprocesses and chunks text, generates embeddings using Sentence Transformers, stores vectors in FAISS, retrieves relevant content through semantic search, expands context using neighboring chunks, and generates grounded answers through an LLM exposed via FastAPI.

---

## 2-Minute Project Explanation

The goal of the project was to build a question-answering system for enterprise documents.

The pipeline begins by loading PDF documents and extracting text. Documents are cleaned and split into overlapping chunks. Each chunk is converted into an embedding using the all-MiniLM-L6-v2 model.

Embeddings are stored inside a FAISS vector index for efficient similarity search.

When a user asks a question:

1. The question is embedded.
2. FAISS retrieves the most relevant chunks.
3. Context expansion adds neighboring chunks.
4. A prompt is constructed.
5. The LLM generates a grounded answer.
6. The API returns both the answer and source chunks.

The application is deployed on Render and exposed through FastAPI.

---

## Key Components

### Document Ingestion

- PyPDF
- PDF text extraction
- Metadata preservation

### Chunking

- Chunk size: 500
- Chunk overlap: 50

### Embeddings

- Sentence Transformers
- all-MiniLM-L6-v2
- 384-dimensional embeddings

### Retrieval

- FAISS similarity search
- Top-K retrieval

### Context Expansion

- Neighbor chunk retrieval
- Improved context continuity

### API

- FastAPI
- REST endpoints

---

## Why Did You Build This?

The project demonstrates:

- Retrieval-Augmented Generation
- Vector databases
- Semantic search
- API development
- Cloud deployment
- AI system design

It represents a realistic enterprise AI use case.

---

## Common Interview Questions

### Why RAG instead of using an LLM directly?

LLMs can hallucinate.

RAG retrieves relevant information before generation, improving accuracy and grounding responses in source documents.

---

### Why use embeddings?

Embeddings capture semantic meaning.

They allow retrieval even when the question wording differs from the document wording.

---

### Why FAISS?

FAISS provides:

- Fast similarity search
- Efficient vector indexing
- Low infrastructure overhead

---

### Why chunk documents?

Large documents reduce retrieval precision.

Chunking improves relevance and retrieval quality.

---

### Why overlap chunks?

Important information may exist at chunk boundaries.

Overlap prevents information loss.

---

### Why context expansion?

Retrieved chunks may be incomplete.

Neighboring chunks often contain supporting information.

---

### Why FastAPI?

FastAPI provides:

- High performance
- Automatic API documentation
- Type validation
- Production readiness

---

### How would you scale this system?

Replace FAISS with:

- Pinecone
- Weaviate

Add:

- Hybrid search
- Reranking
- Distributed indexing
- Kubernetes deployment

---

### Biggest Technical Challenge

Deployment memory constraints.

The Sentence Transformer model caused startup failures.

Solution:

Implemented lazy loading so the embedding model only loads when needed.

---

### What Would You Improve?

- Hybrid search
- Metadata filtering
- User authentication
- Monitoring
- Vector database migration
- Reranking models

---

## Resume Talking Points

- Built an end-to-end Retrieval-Augmented Generation platform.
- Implemented semantic search using FAISS and Sentence Transformers.
- Designed context expansion to improve answer quality.
- Developed FastAPI-based REST APIs.
- Deployed cloud-hosted AI services using Render.
- Improved deployment reliability through lazy-loading optimization.

---

## Technical Keywords

RAG

FAISS

Vector Search

Semantic Search

Embeddings

Sentence Transformers

FastAPI

LLM

Prompt Engineering

Document Chunking

Context Expansion

REST APIs

Render

Python

Enterprise AI