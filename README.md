# Enterprise RAG Assistant

An end-to-end Retrieval-Augmented Generation (RAG) application built with FastAPI, Streamlit, FAISS, Sentence Transformers, Docker, Airflow, and MLflow.

The system ingests enterprise documents, generates embeddings, stores them in a vector database, retrieves relevant context using semantic search, and generates grounded answers using an LLM.

---

## Architecture

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

## Tech Stack

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

---

## Project Structure

```text
enterprise-rag-project/

├── app/
│   ├── api.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retrieval.py
│   ├── rag_pipeline.py
│   ├── vector_store.py
│   └── streamlit_app.py
│
├── dags/
│   └── rag_indexing_dag.py
│
├── data/
│   └── raw/pdf/
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Sample Question

Question:

```text
What is CirQX?
```

Answer:

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

```http
POST /ask
```

Request:

```json
{
  "question": "What is CirQX?"
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

## Future Improvements

- Hybrid Search (Semantic + Keyword)
- Reranking Models
- Production Vector Databases (Pinecone, Weaviate)
- Authentication & Authorization
- AWS ECS Deployment
- Monitoring & Alerting

---

## Author

Poonam Jaiswal

Machine Learning Engineer | AI/ML | Generative AI | RAG Systems

GitHub:
https://github.com/birzu7