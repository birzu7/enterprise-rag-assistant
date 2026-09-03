# Enterprise RAG Assistant

An end-to-end Retrieval-Augmented Generation (RAG) application built with FastAPI, FAISS, Sentence Transformers, Docker, Airflow, and MLflow.

The system ingests enterprise documents, generates embeddings, stores them in a vector database, retrieves relevant context using semantic search, and generates grounded answers using a Large Language Model (LLM).

---

## Overview

Enterprise RAG Assistant enables users to ask natural language questions over enterprise documents.

The platform processes PDF documents, converts them into searchable vector representations, retrieves the most relevant content using semantic similarity search, expands context using neighboring document chunks, and generates context-aware answers.

---

## Architecture

```text
Document PDFs
      ↓
Document Ingestion
      ↓
Text Preprocessing
      ↓
Chunking
      ↓
Embeddings (all-MiniLM-L6-v2)
      ↓
FAISS Vector Store
      ↓
Semantic Retrieval
      ↓
Context Expansion
      ↓
Prompt Builder
      ↓
LLM
      ↓
FastAPI Backend
      ↓
Streamlit Frontend
```

For detailed architecture documentation, see:

- docs/architecture.md

---

## Design Highlights

- Retrieval-Augmented Generation (RAG) architecture
- Semantic search using FAISS
- Context expansion using neighboring chunks
- Modular pipeline design
- REST API powered by FastAPI
- Cloud deployment using Render
- Scalable document ingestion pipeline
- Separation of retrieval and generation layers

---

## Features

- PDF document ingestion
- Text preprocessing and cleaning
- Paragraph-aware document chunking
- Sentence Transformer embeddings
- FAISS vector database
- Semantic similarity search
- Context expansion using neighboring chunks
- Prompt engineering
- LLM-powered answer generation
- FastAPI REST API
- Streamlit chat interface
- MLflow experiment tracking
- Airflow orchestration
- Dockerized deployment

---

## Technology Stack

### AI / Machine Learning

- Sentence Transformers
- FAISS
- Retrieval-Augmented Generation (RAG)

### Backend

- Python
- FastAPI

### Frontend

- Streamlit

### MLOps

- Docker
- Airflow
- MLflow

### Data Processing

- NumPy
- Pandas
- PyPDF

### Deployment

- Render
- GitHub

---

## Project Structure

```text
enterprise-rag-project/

├── app/
│   ├── api.py
│   ├── chunking.py
│   ├── config.py
│   ├── context_expansion.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── load_documents.py
│   ├── preprocess.py
│   ├── prompt_builder.py
│   ├── rag_pipeline.py
│   ├── retrieval.py
│   ├── vector_store.py
│   └── streamlit_app.py
│
├── dags/
│   └── rag_indexing_dag.py
│
├── data/
│   └── raw/pdf/
│
├── docs/
│   ├── architecture.md
│   ├── project-design.md
│   └── interview-notes.md
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## End-to-End Workflow

1. Load PDF documents
2. Extract document text
3. Clean and preprocess content
4. Split documents into chunks
5. Generate embeddings
6. Store vectors in FAISS
7. Accept user question
8. Generate question embedding
9. Retrieve top matching chunks
10. Expand context using neighboring chunks
11. Build LLM prompt
12. Generate answer
13. Return answer with supporting sources

---

## Deployment

The application is deployed on Render using FastAPI.

### Public API

https://enterprise-rag-assistant-hp7u.onrender.com

### Interactive API Documentation

https://enterprise-rag-assistant-hp7u.onrender.com/docs

---

## Sample Question

Question:

```text
What is CirQX?
```

Example Response:

```text
CirQX is an AI-powered retail intelligence and circular commerce platform designed for India's local retail ecosystem.
```

---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/birzu7/enterprise-rag-assistant.git
cd enterprise-rag-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start FastAPI

```bash
python -m uvicorn app.api:app --reload
```

### Start Streamlit

```bash
streamlit run app/streamlit_app.py
```

---

## API Example

### Ask Question

```http
POST /ask
```

Request:

```json
{
  "question": "What are CirQX revenue streams?"
}
```

Response:

```json
{
  "question": "...",
  "answer": "...",
  "sources": [...]
}
```

---

## Documentation

Additional project documentation is available in:

- docs/architecture.md
- docs/project-design.md
- docs/interview-notes.md

---

## Future Improvements

- Hybrid Search (Semantic + Keyword)
- Reranking Models
- Production Vector Databases (Pinecone, Weaviate)
- User Authentication
- Role-Based Access Control
- AWS ECS Deployment
- Monitoring & Alerting
- Evaluation Frameworks
- Multi-Document Ranking
- Streaming Responses

---

## Author

**Poonam Jaiswal**

Machine Learning Engineer | AI/ML | Generative AI | RAG Systems

GitHub:
https://github.com/birzu7