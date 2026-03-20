import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from huggingface_hub import InferenceClient
from chromadb.config import Settings as ChromaSettings
from core.config import settings

# 🔥 NOVO: Embedding custom usando API oficial HF
from langchain_core.embeddings import Embeddings
from huggingface_hub import InferenceClient


class HFCustomEmbeddings(Embeddings):
    def __init__(self, token):
        self.client = InferenceClient(
            provider="hf-inference",
            api_key=token,
        )
        self.model = "sentence-transformers/all-MiniLM-L6-v2"

    def _normalize(self, result):
        # Se vier numpy array → vira lista
        if hasattr(result, "tolist"):
            result = result.tolist()

        # Se vier lista 2D → pega primeira linha
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            result = result[0]

        return result

    def embed_documents(self, texts):
        embeddings = []

        for text in texts:
            result = self.client.feature_extraction(
                text,
                model=self.model
            )

            result = self._normalize(result)
            embeddings.append(result)

        return embeddings

    def embed_query(self, text):
        result = self.client.feature_extraction(
            text,
            model=self.model
        )

        return self._normalize(result)


def ingest_docs():
    # 1. Carregar PDFs
    print("--- Iniciando carregamento de PDFs ---")
    loader = DirectoryLoader(settings.DOCS_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    # 2. Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"--- {len(chunks)} blocos de texto gerados ---")

    # 3. Embeddings via API HF (FIX DEFINITIVO)
    print("--- Configurando API de Embeddings (Hugging Face - Router) ---")

    embeddings = HFCustomEmbeddings(settings.HUGGINGFACE_TOKEN)

    # 4. Banco vetorial
    print("--- Criando banco de dados vetorial em /chroma_db ---")

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.CHROMA_PATH,
        collection_name="racs_collection",
        client_settings=ChromaSettings(
            anonymized_telemetry=False,
            is_persistent=True
        )
    )

    vector_db.persist()

    print("--- Ingestão concluída com sucesso! ---")
    return vector_db