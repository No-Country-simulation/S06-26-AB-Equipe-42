"""
Repositório de Concentração de Utilizadores.
Responsável pela leitura dos dados de tráfego, congestionamento e qualidade de sinal.
Responsável: Domingos Kapipa Chivela (implementação real com Supabase).
             Willfredy Vieira Dias (esqueleto e contrato de interface).
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def obter_concentracao_por_regiao(regiao_id: int, periodo: Optional[str] = None) -> list[dict]:
    """
    Retorna os dados de concentração e qualidade de rede para uma região específica.

    Args:
        regiao_id: Identificador único da região/cluster.
        periodo: Período do dia ('manha', 'tarde', 'noite'). None = todos os períodos.

    Returns:
        Lista de registos com n_usuarios, congestionamento_medio, drop_pct_medio, day_date.
    """
    # TODO: Substituir por query real ao Supabase (Domingos)
    # Exemplo de implementação futura:
    # from app.db.session import get_supabase_client
    # client = get_supabase_client()
    # query = client.table("concentracao").select("*").eq("ecgi", ecgi)
    # if periodo:
    #     query = query.eq("periodo", periodo)
    # resultado = query.execute()
    # return resultado.data
    logger.warning("concentracao_repo: a usar dados mock. Substituir por Supabase (Domingos).")
    return []


async def obter_top_regioes_por_indicador(indicador: str, limite: int = 10) -> list[dict]:
    """
    Retorna as regiões com valores mais elevados para um indicador específico.

    Args:
        indicador: Nome do campo a ordenar (ex: 'n_usuarios', 'congestionamento_medio').
        limite: Número máximo de resultados a devolver.

    Returns:
        Lista de registos ordenados do maior para o menor valor do indicador.
    """
    # TODO: Substituir por query real ao Supabase com ORDER BY e LIMIT (Domingos)
    logger.warning("concentracao_repo.obter_top_regioes_por_indicador: mock a retornar lista vazia.")
    return []


async def obter_concentracao_por_municipio(municipio: str, periodo: Optional[str] = None) -> list[dict]:
    """
    Retorna os dados de concentração para todas as regiões de um município.

    Args:
        municipio: Nome do município (ex: 'Cazenga', 'Viana').
        periodo: Período do dia ('manha', 'tarde', 'noite'). None = todos.

    Returns:
        Lista de registos de concentração do município.
    """
    # TODO: Substituir por query real ao Supabase com JOIN regioes (Domingos)
    logger.warning("concentracao_repo.obter_concentracao_por_municipio: mock a retornar lista vazia.")
    return []
