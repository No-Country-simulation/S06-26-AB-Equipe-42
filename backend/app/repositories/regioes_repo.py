"""
Repositório de Regiões/Clusters.
Responsável pela leitura dos dados de regiões geográficas da base de dados.
Responsável: Domingos Kapipa Chivela (implementação real com Supabase).
             Willfredy Vieira Dias (esqueleto e contrato de interface).
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def obter_todas_regioes() -> list[dict]:
    """
    Retorna todas as regiões/clusters registados na base de dados.

    Returns:
        Lista de dicionários com os campos:
        id, nome_cluster, municipio, lat_centro, lon_centro, perfil.
    """
    # TODO: Substituir por query real ao Supabase (Domingos)
    # Exemplo de implementação futura:
    # from app.db.session import get_supabase_client
    # client = get_supabase_client()
    # resultado = client.table("regioes").select("*").execute()
    # return resultado.data
    logger.warning("regioes_repo: a usar dados mock. Substituir por Supabase (Domingos).")
    return []


async def obter_regiao_por_id(regiao_id: int) -> Optional[dict]:
    """
    Retorna os dados de uma região específica pelo seu ID.

    Args:
        regiao_id: Identificador único da região.

    Returns:
        Dicionário com os dados da região, ou None se não encontrada.
    """
    # TODO: Substituir por query real ao Supabase (Domingos)
    logger.warning("regioes_repo.obter_regiao_por_id: mock a retornar None.")
    return None


async def obter_regioes_por_municipio(municipio: str) -> list[dict]:
    """
    Retorna todas as regiões/clusters pertencentes a um município específico.

    Args:
        municipio: Nome do município (ex: 'Cazenga', 'Viana').

    Returns:
        Lista de regiões no município indicado.
    """
    # TODO: Substituir por query real ao Supabase (Domingos)
    logger.warning("regioes_repo.obter_regioes_por_municipio: mock a retornar lista vazia.")
    return []
