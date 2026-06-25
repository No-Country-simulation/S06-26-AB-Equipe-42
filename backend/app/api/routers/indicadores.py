"""
Router de suporte: metadados dos indicadores disponíveis na plataforma.
Permite ao frontend apresentar corretamente os filtros e legendas do mapa.
"""

from fastapi import APIRouter
from app.models.schemas import IndicadoresResponse, IndicatorMetadata

router = APIRouter()

_INDICADORES = [
    IndicatorMetadata(
        id="n_usuarios",
        nome="Número de Utilizadores",
        descricao="Volume de utilizadores móveis ativos registados na região durante o período analisado.",
    ),
    IndicatorMetadata(
        id="congestionamento_medio",
        nome="Congestionamento Médio",
        descricao="Taxa média de congestionamento dos canais de tráfego (0.0 = sem congestionamento, 1.0 = saturado).",
    ),
    IndicatorMetadata(
        id="cobertura_sinal_dbm",
        nome="Nível de Sinal (dBm)",
        descricao="Qualidade média da cobertura de rede medida em decibéis-miliwatts. Valores mais próximos de 0 indicam melhor cobertura.",
    ),
]


@router.get("/indicadores", response_model=IndicadoresResponse)
async def listar_indicadores():
    """
    Retorna os metadados de todos os indicadores suportados pela plataforma.
    Utilizado pelo frontend para apresentar legendas e filtros contextualizados.
    """
    return IndicadoresResponse(indicadores=_INDICADORES)
