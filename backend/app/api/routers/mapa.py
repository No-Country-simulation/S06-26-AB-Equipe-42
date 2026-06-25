"""
Router do mapa interativo.
Retorna as coordenadas geográficas e indicadores consolidados
de todas as regiões/clusters para renderização no mapa Leaflet.
Responsável: Willfredy (orquestração) — dados reais: Domingos.
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.models.schemas import MapaResponse, RegionMapData

router = APIRouter()

# Dados mock com coordenadas reais de municípios de Angola
_MOCK_MAPA_DATA = [
    RegionMapData(id=1, nome_cluster="Cazenga_1", municipio="Cazenga",
                  latitude=-8.8123, longitude=13.2945, perfil="Residencial denso",
                  n_usuarios=3800, congestionamento_medio=0.45, cobertura_sinal_dbm=-95.2),
    RegionMapData(id=2, nome_cluster="Viana_Centro", municipio="Viana",
                  latitude=-8.9012, longitude=13.3854, perfil="Industrial / Comercial",
                  n_usuarios=4500, congestionamento_medio=0.35, cobertura_sinal_dbm=-102.0),
    RegionMapData(id=3, nome_cluster="Luanda_Norte", municipio="Luanda",
                  latitude=-8.7600, longitude=13.2300, perfil="Urbano central",
                  n_usuarios=6200, congestionamento_medio=0.68, cobertura_sinal_dbm=-88.5),
    RegionMapData(id=4, nome_cluster="Cacuaco_1", municipio="Cacuaco",
                  latitude=-8.7870, longitude=13.3670, perfil="Periurbano",
                  n_usuarios=2100, congestionamento_medio=0.22, cobertura_sinal_dbm=-107.3),
    RegionMapData(id=5, nome_cluster="Belas_Sul", municipio="Belas",
                  latitude=-8.9500, longitude=13.2100, perfil="Residencial médio",
                  n_usuarios=1850, congestionamento_medio=0.18, cobertura_sinal_dbm=-99.1),
]


@router.get("/mapa", response_model=MapaResponse)
async def obter_dados_mapa(
    indicador: Optional[str] = Query(
        None,
        description="Filtro por indicador (ex: n_usuarios, congestionamento_medio, cobertura_sinal_dbm)."
    )
):
    """
    Retorna coordenadas geográficas e indicadores de todas as regiões/clusters
    para renderização no mapa interativo Leaflet do frontend.
    """
    # TODO: Substituir dados mock por consulta real ao repositório (Domingos)
    return MapaResponse(regioes=_MOCK_MAPA_DATA)
