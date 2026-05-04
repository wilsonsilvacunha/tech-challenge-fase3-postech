import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.langgraph_flows.fluxos import consultar

st.set_page_config(
    page_title="Assistente de Saúde da Mulher",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Assistente Virtual — Saúde da Mulher")
st.caption("Powered by LangChain + LangGraph + Groq (LLaMA3)")

if "historico" not in st.session_state:
    st.session_state.historico = []

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pergunta = st.chat_input("Digite sua pergunta sobre saúde da mulher...")

if pergunta:
    with st.chat_message("user"):
        st.write(pergunta)
    st.session_state.historico.append({"role": "user", "content": pergunta})

    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            resultado = consultar(pergunta)
            resposta = resultado["resposta"]
            categoria = resultado["categoria"].upper()
            encaminhamento = resultado["encaminhamento"]

            st.write(resposta)
            st.info(f"📂 Categoria: {categoria} | 📋 {encaminhamento}")

    st.session_state.historico.append({"role": "assistant", "content": resposta})
