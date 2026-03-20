import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "RAC's-IA"
    
    # Chaves de API (Puxando do .env)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN") 
    
    # Configurações de Caminhos
    CHROMA_PATH: str = "chroma_db"
    DOCS_PATH: str = "docs"
    
    # Modelos
    # Modelo Groq (LLM para o chat)
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    # Modelo HuggingFace (Para Embeddings via API)
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

settings = Settings()