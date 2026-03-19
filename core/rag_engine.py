from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from core.config import settings
from chromadb.config import Settings

def get_rag_response(user_question: str):
    # 1. Embeddings e Banco de Dados
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(
        persist_directory=settings.CHROMA_PATH,
        embedding_function=embeddings,
        client_settings=Settings(anonymized_telemetry=False)
    )

    # 2. Configurar o LLM
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.MODEL_NAME,
        temperature=0.1
    )

    # 3. Novo jeito de montar o Prompt
    # O novo sistema pede um input chamado {context} e {input}
    system_prompt = (
        "Você é um assistente virtual da RAC's-IA, especialista técnico nas Normas de Atividades Críticas (RAC) "
        "Seu objetivo é fornecer informações precisas baseadas nos documentos oficiais de segurança. Use os trechos abaixo para responder. Se não souber, diga que não encontrou nas normas. "
        "Contexto: {context}"
    )
    
    prompt = PromptTemplate.from_template(
        template=system_prompt + "\n\nPergunta: {input}\nResposta:"
    )

    # 4. Criar a "Cadeia de Documentos" (Como a IA lê os textos)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)

    # 5. Criar a "Cadeia de Recuperação" (O que une o Banco + LLM)
    # Note que agora o RetrievalQA foi substituído por isso aqui:
    retrieval_chain = create_retrieval_chain(
        vector_db.as_retriever(search_kwargs={"k": 4}), 
        combine_docs_chain
    )

    # 6. Executar (Agora o campo se chama 'input' e a resposta vem em 'answer')
    response = retrieval_chain.invoke({"input": user_question})
    
    return response["answer"]