from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_pipeline import answer_question


app = FastAPI(
    title="Enterprise RAG API",
    description="API for the Enterprise RAG project",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to the Enterprise RAG API!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = answer_question(
        question=request.question
    )

    return result