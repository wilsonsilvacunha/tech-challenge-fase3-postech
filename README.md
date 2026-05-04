# 🏥 Assistente Virtual — Saúde da Mulher

**Tech Challenge Fase 3 | POSTECH IA para Devs**

Sistema de assistência clínica especializado em saúde da mulher, desenvolvido com **LangChain**, **LangGraph** e **LLaMA-3.1** (via Groq). Implementa pipeline de recuperação aumentada por geração (RAG) sobre protocolos médicos especializados, com quatro fluxos automatizados de decisão clínica.

## 🚀 Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/wilsonsilvacunha/tech-challenge-fase3-postech.git
cd tech-challenge-fase3-postech

# 2. Instale as dependências
pip install langchain langchain-groq langchain-community langchain-text-splitters langgraph chromadb sentence-transformers streamlit

# 3. Configure a API Key
echo "GROQ_API_KEY=sua_chave_aqui" > .env

# 4. Execute
streamlit run app.py
```

## 🛠️ Stack Técnica

- **LLM:** LLaMA-3.1-8B (Groq)
- **Orquestração:** LangChain
- **Fluxos:** LangGraph
- **Interface:** Streamlit

## ⚠️ Aviso

Este sistema é um assistente de apoio informativo. Não substitui consulta médica presencial.
