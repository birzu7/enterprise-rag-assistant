# Enterprise RAG Assistant Architecture

## Purpose

Enterprise RAG Assistant enables users to ask natural language questions over enterprise documents and receive grounded answers based on document content.

The system combines document retrieval and Large Language Models (LLMs) to reduce hallucinations and improve answer accuracy.

---

## High-Level Architecture

```text
PDF Documents
      ↓
Document Loader
      ↓
Preprocessing
      ↓
Chunking
      ↓
Embedding Generation
      ↓
FAISS Vector Store
      ↓
Question Embedding
      ↓
Semantic Retrieval
      ↓
Context Expansion
      ↓
Prompt Builder
      ↓
LLM
      ↓
Generated Answer
```

---

## Component Overview

### 1. Document Loader

File:
`load_documents.py`

Responsibilities:

- Load PDF documents
- Extract text using PyPDF
- Preserve metadata
- Pass documents for preprocessing

---

### 2. Preprocessing

File:
`preprocess.py`

Responsibilities:

- Clean document text
- Remove unnecessary whitespace
- Normalize formatting

---

### 3. Chunking

File:
`chunking.py`

Responsibilities:

- Split large documents into manageable chunks
- Preserve context overlap
- Generate chunk metadata

Configuration:

- Chunk Size: 500 characters
- Chunk Overlap: 50 characters

---

### 4. Embedding Generation

File:
`embeddings.py`

Responsibilities:

- Convert text into dense vector embeddings
- Generate embeddings for document chunks
- Generate embeddings for user questions

Model:

- all-MiniLM-L6-v2

Embedding Dimension:

- 384

---

### 5. Vector Store

File:
`vector_store.py`

Responsibilities:

- Store embeddings in FAISS
- Persist vector index
- Load index during retrieval

Technology:

- FAISS

---

### 6. Semantic Retrieval

File:
`retrieval.py`

Responsibilities:

- Embed user question
- Search FAISS index
- Return top matching chunks

Output:

- Similarity score
- Source metadata
- Chunk text

---

### 7. Context Expansion

File:
`context_expansion.py`

Responsibilities:

- Expand retrieved chunks
- Include neighboring chunks
- Improve answer completeness

Benefits:

- Preserves local document context
- Reduces fragmented answers

---

### 8. Prompt Builder

File:
`prompt_builder.py`

Responsibilities:

- Combine retrieved context
- Construct LLM prompt
- Enforce grounded answering

---

### 9. LLM Layer

File:
`llm.py`

Responsibilities:

- Generate final answer
- Use retrieved context only
- Return human-readable response

---

### 10. API Layer

File:
`api.py`

Responsibilities:

- Accept user questions
- Execute RAG pipeline
- Return answer and sources

Framework:

- FastAPI

Endpoints:

GET /

POST /ask

---

## Data Flow

### Indexing Flow

```text
PDF
 ↓
Preprocessing
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Index
```

### Query Flow

```text
Question
 ↓
Question Embedding
 ↓
FAISS Search
 ↓
Context Expansion
 ↓
Prompt Builder
 ↓
LLM
 ↓
Answer
```

---

## Deployment Architecture

```text
GitHub
   ↓
Render
   ↓
FastAPI Application
   ↓
Public REST API
```

---

## Scalability Improvements

Future enhancements:

- Hybrid Search
- Reranking Models
- Pinecone Vector Database
- Weaviate
- Metadata Filtering
- Streaming Responses
- Authentication
- Monitoring and Observability