from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.3
)

SYSTEM_PROMPT = """Você é um assistente virtual especializado em saúde da mulher, desenvolvido para apoiar profissionais de saúde e pacientes com informações baseadas em evidências clínicas. Suas áreas de atuação incluem: Ginecologia e obstetrícia, Prevenção (mamografia, papanicolau, vacinação), Saúde mental feminina, Planejamento familiar e contracepção, Identificação de situações de violência doméstica. REGRAS: 1) Nunca prescreva medicamentos. 2) Oriente atendimento presencial em casos urgentes. 3) Em violência doméstica, forneça o número 180. 4) Cite protocolos do Ministério da Saúde quando aplicável."""

historico = []

def perguntar(pergunta: str) -> str:
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            *[(("human" if isinstance(m, HumanMessage) else "assistant"), m.content) for m in historico[-10:]],
            ("human", "{input}")
        ])
        chain = prompt | llm
        resposta = chain.invoke({"input": pergunta})
        historico.append(HumanMessage(content=pergunta))
        historico.append(AIMessage(content=resposta.content))
        return resposta.content
    except Exception as e:
        return f"Erro: {str(e)}"
