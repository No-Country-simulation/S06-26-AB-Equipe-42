"""
Router de consulta inteligente — endpoint principal da plataforma.
Orquestra o fluxo completo:
  1. Interpreta a consulta em linguagem natural (llm_service)
  2. Pesquisa dados reais do dataset Vísent (data_service)
  3. Sintetiza a resposta em linguagem natural (llm_service)

Responsável: Willfredy Vieira Dias (orquestração completa).
"""

import logging

from fastapi import APIRouter, HTTPException

from app.models.schemas import QueryRequest, QueryResponse
from app.services import llm_service, data_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/dados", response_model=QueryResponse)
async def consultar_dados(pedido: QueryRequest):
    """
    Endpoint principal de consulta inteligente.

    Recebe uma pergunta em linguagem natural, interpreta-a via LLM,
    pesquisa os dados relevantes no dataset Vísent e devolve uma síntese
    textual com os dados em bruto e as fontes utilizadas.
    """
    logger.info("Nova consulta recebida: '%s' (idioma: %s)", pedido.consulta, pedido.idioma)

    # --- Etapa 1: Interpretar a consulta ---
    try:
        parametros = await llm_service.interpretar_consulta(
            texto=pedido.consulta,
            idioma=pedido.idioma or "pt",
        )
        logger.info("Parâmetros extraídos: %s", parametros)
    except Exception as e:
        logger.error("Falha na interpretação da consulta: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="Falha na comunicação com o serviço de inteligência artificial.",
        )

    # --- Verificação de confiança: pede esclarecimento se muito baixa ---
    # Nota: confianca == 0.0 indica erro do LLM (fallback mock) — não bloquear
    confianca = parametros.get("confianca", 1.0)
    is_mock = parametros.get("mock", False)
    if isinstance(confianca, (int, float)) and confianca < 0.3 and not is_mock and confianca != 0.0:
        raise HTTPException(
            status_code=400,
            detail=(
                "Não consegui interpretar a sua consulta com confiança suficiente. "
                "Pode reformulá-la? Por exemplo: "
                "'Qual o cluster com maior congestionamento durante a tarde?'"
            ),
        )

    # --- Etapa 2: Pesquisar dados reais ---
    # Funde os filtros estruturados do utilizador com os parâmetros extraídos pelo LLM
    parametros_finais = {**parametros, **(pedido.filtros or {})}
    try:
        dados, fontes = await data_service.pesquisar_dados(parametros_finais)
    except Exception as e:
        logger.error("Falha na pesquisa de dados: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="Erro ao aceder à base de dados. Tente novamente.",
        )

    if not dados:
        return QueryResponse(
            resposta_ia=(
                "Não foram encontrados dados para a sua consulta com os filtros indicados. "
                "Experimente remover filtros ou reformular a pergunta."
            ),
            dados=[],
            fontes=fontes,
        )

    # --- Etapa 3: Sintetizar a resposta ---
    try:
        resposta_texto = await llm_service.sintetizar_resposta(
            dados=dados,
            pergunta_original=pedido.consulta,
            idioma=pedido.idioma or "pt",
        )
    except Exception as e:
        logger.error("Falha na síntese da resposta: %s", str(e))
        # Degradação graciosa: devolve os dados sem síntese textual
        resposta_texto = (
            "Não foi possível gerar a síntese automática. "
            "Os dados em bruto estão disponíveis abaixo."
        )

    logger.info("Consulta concluída com %d registos.", len(dados))

    return QueryResponse(
        resposta_ia=resposta_texto,
        dados=dados,
        fontes=fontes,
    )
