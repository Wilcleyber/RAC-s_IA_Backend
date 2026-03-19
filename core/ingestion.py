import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from core.config import settings

def ingest_docs():
    # 1. Carregar todos os PDFs da pasta /docs
    print("--- Iniciando carregamento de PDFs ---")
    loader = DirectoryLoader(settings.DOCS_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    # 2. Dividir o texto em blocos (Chunks)
    # Isso evita que o texto seja longo demais para o LLM processar
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"--- {len(chunks)} blocos de texto gerados ---")

    # 3. Criar o Modelo de Embeddings
    # Usamos um modelo gratuito da HuggingFace que roda localmente
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Criar e Persistir o Banco de Dados Vetorial (ChromaDB)
    print("--- Criando banco de dados vetorial em /chroma_db ---")
    vector_db = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=settings.CHROMA_PATH,
        client_settings=Settings(anonymized_telemetry=False, allow_reset=True)
    )
    
    print("--- Ingestão concluída com sucesso! ---")
    return vector_db

if __name__ == "__main__":
    # Teste rápido: se rodar este arquivo sozinho, ele processa os docs
    ingest_docs()