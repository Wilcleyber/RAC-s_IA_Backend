import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "RAC's-IA"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    # Caminho onde os vetores serão salvos
    CHROMA_PATH: str = "chroma_db"
    # Caminho onde os PDFs das RACs devem estar
    DOCS_PATH: str = "docs"
    # Modelo de LLM da Groq
    MODEL_NAME: str = "llama-3.3-70b-versatile"

settings = Settings()