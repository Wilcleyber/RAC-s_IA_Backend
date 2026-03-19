# RAC's-IA - Backend 🛡️🧠

O **RAC's-IA** é o motor de inteligência artificial desenvolvido para consulta técnica das Normas de Atividades Críticas (RAC). Utiliza a arquitetura **RAG (Retrieval-Augmented Generation)** para fornecer respostas precisas baseadas em documentos oficiais.

## 🚀 Tecnologias Utilizadas
* **FastAPI**: Framework web de alta performance.
* **LangChain**: Orquestração da lógica de IA e RAG.
* **ChromaDB**: Banco de dados vetorial para busca semântica.
* **Groq (Llama 3.3)**: Modelo de linguagem de baixa latência para geração de respostas.
* **Pydantic**: Validação de dados e configurações.

## 🛠️ Estratégia de Implementação
Este backend foi construído focando em estabilidade e segurança:
* Isola as normas técnicas para evitar alucinações da IA.
* Implementa CORS para comunicação segura com o Frontend.
* Gerenciamento de dependências via ambiente virtual isolado.

## 📦 Teste Swagger



---
*Desenvolvido por Wilcleyber - Estudante de ADS na Uninassau.*