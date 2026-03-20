# RAC's-IA - Backend 🛡️🧠

O **RAC's-IA** é o motor de inteligência artificial de alta performance desenvolvido para consulta técnica das Normas de Atividades Críticas (RAC). O sistema utiliza a arquitetura **RAG (Retrieval-Augmented Generation)** para garantir respostas técnicas e seguras baseadas exclusivamente em documentos oficiais.

## 🚀 Diferenciais de Engenharia
Diferente de implementações padrão, este projeto foi otimizado para **máxima eficiência em ambientes de recursos limitados** (como o Render Free Tier):

* **Custom Embedding Wrapper:** Desenvolvemos uma classe personalizada (`HFCustomEmbeddings`) que se comunica diretamente com a **Hugging Face Inference API**. Isso eliminou conflitos de dependências externas e reduziu o consumo de RAM de **500MB para <100MB**.
* **Arquitetura Híbrida e Leve:** O backend atua como um orquestrador estratégico, delegando o processamento pesado de vetores e inferência para infraestruturas globais (**Hugging Face** e **Groq**), garantindo latência mínima.
* **Consistência Vetorial:** Implementação de normalização de tipos (`NumPy Array` para `Python List`) para garantir 100% de compatibilidade com o **ChromaDB**.

## 🛠️ Stack Tecnológica
* **FastAPI**: Framework assíncrono de alta performance.
* **LangChain**: Orquestração avançada da lógica RAG.
* **ChromaDB**: Banco de dados vetorial (Vector Store) para busca semântica.
* **Groq (Llama 3.3 - 70B)**: Inferência de linguagem ultra-rápida.
* **Hugging Face API**: Geração de embeddings via Cloud.

## 🏗️ Estratégia de Segurança e Confiabilidade
* **Zero Alucinação:** O sistema é instruído a responder estritamente com base no contexto das normas carregadas.
* **Persistent Client:** Conexão ríguida com o banco vetorial para evitar falhas de telemetria e corrupção de dados.
* **CORS & Pydantic:** Camadas de segurança para comunicação com o Frontend e validação rigorosa de dados.

## 📦 Documentação da API (Swagger)
Acesse e teste os endpoints em tempo real:
👉 [https://rac-s-ia.onrender.com/docs](https://rac-s-ia.onrender.com/docs)

---
*Desenvolvido por **Wilcleyber** - Estudante de ADS na Uninassau (2º Ano).*