import chromadb
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from chromadb.config import Settings as ChromaSettings
from core.config import settings

# 🔥 IMPORTA O MESMO EMBEDDING CUSTOM
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
        if hasattr(result, "tolist"):
            result = result.tolist()

        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            result = result[0]

        return result

    def embed_documents(self, texts):
        return [self._normalize(
            self.client.feature_extraction(text, model=self.model)
        ) for text in texts]

    def embed_query(self, text):
        return self._normalize(
            self.client.feature_extraction(text, model=self.model)
        )


def get_rag_response(user_question: str):
    # 1. Embeddings (MESMO DA INGESTÃO)
    embeddings = HFCustomEmbeddings(settings.HUGGINGFACE_TOKEN)

    # 2. Cliente Chroma
    client = chromadb.PersistentClient(
        path=settings.CHROMA_PATH,
        settings=ChromaSettings(anonymized_telemetry=False)
    )

    # 3. Vector Store
    vector_db = Chroma(
        client=client,
        embedding_function=embeddings,
        collection_name="racs_collection"
    )

    # 🔥 melhoria: busca mais relevante
    retriever = vector_db.as_retriever(search_kwargs={"k": 4})

    # 4. LLM (Groq)
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.MODEL_NAME,
        temperature=0.1
    )

    # 5. Prompt (levemente melhorado 👀)
    system_prompt = (
        "Você é o assistente virtual da RAC's-IA, especialista técnico nas Normas de Atividades Críticas (RAC).\n"
        "Responda com precisão e objetividade com base APENAS no contexto fornecido.\n"
        "Se a resposta não estiver no contexto, diga claramente que não encontrou essa informação.\n\n"
        "Contexto:\n{context}"
    )

    prompt = PromptTemplate.from_template(
        system_prompt + "\n\nPergunta: {input}\nResposta:"
    )

    # 6. Cadeias
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)

    retrieval_chain = create_retrieval_chain(
        retriever,
        combine_docs_chain
    )

    # 7. Execução
    response = retrieval_chain.invoke({"input": user_question})

    return response["answer"]