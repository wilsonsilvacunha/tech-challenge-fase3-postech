from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from src.langchain_pipeline.assistente import perguntar

class EstadoConsulta(TypedDict):
    pergunta: str
    categoria: str
    resposta: str
    urgente: bool
    encaminhamento: str

def classificar(estado: EstadoConsulta) -> EstadoConsulta:
    p = estado["pergunta"].lower()
    if any(w in p for w in ["violência", "agressão", "machucou", "ameaça", "agrediu", "bateu", "abuso", "marido"]):
        estado["categoria"] = "violencia"
        estado["urgente"] = True
    elif any(w in p for w in ["grávida", "gestação", "pré-natal", "parto"]):
        estado["categoria"] = "obstetrico"
        estado["urgente"] = False
    elif any(w in p for w in ["depressão", "ansiedade", "tristeza", "pós-parto"]):
        estado["categoria"] = "saude_mental"
        estado["urgente"] = False
    elif any(w in p for w in ["mamografia", "papanicolau", "prevenção", "exame"]):
        estado["categoria"] = "prevencao"
        estado["urgente"] = False
    else:
        estado["categoria"] = "geral"
        estado["urgente"] = False
    return estado

def rotear(estado: EstadoConsulta) -> Literal["violencia", "obstetrico", "saude_mental", "prevencao", "geral"]:
    return estado["categoria"]

def atender_violencia(estado: EstadoConsulta) -> EstadoConsulta:
    estado["encaminhamento"] = "URGENTE: Ligue 180 - Central de Atendimento à Mulher"
    estado["resposta"] = perguntar(estado["pergunta"]) + "\n\n⚠️ " + estado["encaminhamento"]
    return estado

def atender_obstetrico(estado: EstadoConsulta) -> EstadoConsulta:
    estado["encaminhamento"] = "Consulte seu obstetra regularmente conforme protocolo pré-natal"
    estado["resposta"] = perguntar(estado["pergunta"])
    return estado

def atender_saude_mental(estado: EstadoConsulta) -> EstadoConsulta:
    estado["encaminhamento"] = "Considere acompanhamento com psicólogo ou psiquiatra"
    estado["resposta"] = perguntar(estado["pergunta"])
    return estado

def atender_prevencao(estado: EstadoConsulta) -> EstadoConsulta:
    estado["encaminhamento"] = "Agende seus exames preventivos na UBS mais próxima"
    estado["resposta"] = perguntar(estado["pergunta"])
    return estado

def atender_geral(estado: EstadoConsulta) -> EstadoConsulta:
    estado["encaminhamento"] = "Em caso de dúvidas, consulte um profissional de saúde"
    estado["resposta"] = perguntar(estado["pergunta"])
    return estado

def criar_grafo():
    grafo = StateGraph(EstadoConsulta)
    grafo.add_node("classificar", classificar)
    grafo.add_node("violencia", atender_violencia)
    grafo.add_node("obstetrico", atender_obstetrico)
    grafo.add_node("saude_mental", atender_saude_mental)
    grafo.add_node("prevencao", atender_prevencao)
    grafo.add_node("geral", atender_geral)
    grafo.set_entry_point("classificar")
    grafo.add_conditional_edges("classificar", rotear)
    for no in ["violencia", "obstetrico", "saude_mental", "prevencao", "geral"]:
        grafo.add_edge(no, END)
    return grafo.compile()

assistente = criar_grafo()

def consultar(pergunta: str) -> dict:
    estado_inicial = {
        "pergunta": pergunta,
        "categoria": "",
        "resposta": "",
        "urgente": False,
        "encaminhamento": ""
    }
    return assistente.invoke(estado_inicial)
