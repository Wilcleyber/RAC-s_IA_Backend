from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.config import settings
from core.rag_engine import get_rag_response 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

origins = [
    "http://localhost:5173",
    "https://rac-ia.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    # Esse endpoint é o que o Render usa para saber que o app está vivo!
    return {"status": "online", "project": settings.PROJECT_NAME}

@app.get("/health")
def health_check():
    # Este é o endpoint que o seu Hook useHealthCheck vai bater
    return {"status": "online", "project": settings.PROJECT_NAME}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Aqui o RAG Engine assume o comando
        answer = get_rag_response(request.question)
        return {"answer": answer}
    except Exception as e:
        print(f"ERRO NO CHAT: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# REMOVEMOS O ENDPOINT /INGEST DAQUI POR SEGURANÇA NO RENDER
# A ingestão deve ser feita localmente para não estourar o timeout do Render.