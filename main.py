from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.config import settings
from core.ingestion import ingest_docs
from core.rag_engine import get_rag_response # Novo import
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # No início deixamos "*" para aceitar qualquer origem
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"], # Permite todos os headers
)

# Modelo de dados para a pergunta
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"status": "online", "project": settings.PROJECT_NAME}

@app.post("/ingest")
def run_ingestion():
    try:
        ingest_docs()
        return {"message": "Documentos processados com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        answer = get_rag_response(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))