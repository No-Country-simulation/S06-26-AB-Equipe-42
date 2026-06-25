"""
Repositório de Indicadores Externos.
Responsável pela leitura de indicadores complementares (ex: desemprego, IDH).
Responsável: Domingos Kapipa Chivela (implementação real com Supabase).
             Willfredy Vieira Dias (esqueleto e contrato de interface).
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def obter_indicadores_por_regiao(regiao_id: int) -> list[dict]:
    """
    Retorna indicadores externos (ex: desemprego, IDH) para uma região.

    Args:
        regiao_id: Identificador único da região.

    Returns:
        Lista de indicadores com tipo, valor, fonte e flag is_mock.
    """
    # TODO: Substituir por query real ao Supabase (Domingos)
    # Exemplo:
    # client.table("indicadores_externos").select("*").eq("regiao_id", regiao_id).execute()
    logger.warning("indicadores_repo: a usar dados mock. Substituir por Supabase (Domingos).")
    return [
        {
            "regiao_id": regiao_id,
            "tipo": "taxa_desemprego",
            "valor": 12.5,
            "fonte": "IBGE 2022 (mock)",
            "is_mock": True,
        }
    ]


async def obter_todos_indicadores() -> list[dict]:
    """
    Retorna todos os indicadores externos registados no sistema.

    Returns:
        Lista completa de indicadores com flag is_mock para transparência.
    """
    # TODO: Substituir por query real ao Supabase (Domingos)
    logger.warning("indicadores_repo.obter_todos_indicadores: mock a retornar lista vazia.")
    return []
