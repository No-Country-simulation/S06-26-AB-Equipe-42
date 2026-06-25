"""
Router de consulta inteligente — endpoint principal da plataforma.
Recebe perguntas em linguagem natural, interpreta-as via LLM,
consulta a base de dados e devolve uma síntese com dados e fontes.
Responsável: Willfredy (orquestração completa).
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import QueryRequest, QueryResponse, SourceInfo

router = APIRouter()


@router.post("/dados", response_model=QueryResponse)
async def consultar_dados(pedido: QueryRequest):
    """
    Orquestra o fluxo completo de consulta inteligente:
    1. Interpreta a consulta em linguagem natural (LLM).
    2. Pesquisa os dados relevantes na base de dados.
    3. Sintetiza uma resposta em linguagem natural com citações.
    """
    # TODO: Integrar com llm_service.interpretar_consulta (Edivaldo)
    # TODO: Integrar com data_service / repositórios (Domingos)
    # TODO: Integrar com llm_service.sintetizar_resposta (Edivaldo)

    # Resposta mock temporária para validar o fluxo fim-a-fim
    return QueryResponse(
        resposta_ia=(
            f"[Mock] Recebi a sua consulta: '{pedido.consulta}'. "
            f"Filtros aplicados: {pedido.filtros}. Idioma: {pedido.idioma}. "
            "A integração com o agente de IA será implementada no Componente 6."
        ),
        dados=[
            {
                "regiao_id": 1,
                "nome_cluster": "Cazenga_1",
                "municipio": "Cazenga",
                "n_usuarios": 3800,
                "congestionamento_medio": 0.45,
                "cobertura_sinal_dbm": -95.2,
            }
        ],
        fontes=[
            SourceInfo(
                tabela="concentracao",
                descricao="Dados mock — integração real pendente (Componente 6)."
            )
        ],
    )
