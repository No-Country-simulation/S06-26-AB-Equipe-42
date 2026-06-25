"""
Router do mapa interativo.
Retorna as coordenadas geográficas e indicadores consolidados de todas as regiões/clusters
para renderização no mapa Leaflet do frontend.

Utiliza dados reais do tensor_concentracao.csv (dataset Vísent).
Responsável: Willfredy Vieira Dias.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Query

from app.models.schemas import MapaResponse, RegionMapData
from app.services.data_service import _carregar_concentracao, _agregar_por_cluster

logger = logging.getLogger(__name__)
router = APIRouter()

# Referência dos 27 clusters com coordenadas reais (CDRView TechRef v2 — Secção 12)
_CLUSTER_COORDS = {
    "CBD_BEIRAMAR":          {"lat": -27.5954, "lon": -48.5480, "perfil": "Centro corporativo"},
    "CENTRO_HISTORICO":      {"lat": -27.5970, "lon": -48.5482, "perfil": "Turismo / serviços"},
    "TRINDADE":              {"lat": -27.6011, "lon": -48.5320, "perfil": "Residencial universitário"},
    "UFSC":                  {"lat": -27.5969, "lon": -48.5500, "perfil": "Campus universitário"},
    "COQUEIROS":             {"lat": -27.5820, "lon": -48.5700, "perfil": "Residencial classe A"},
    "ESTREITO_CAPOEIRAS":    {"lat": -27.5880, "lon": -48.5850, "perfil": "Corredor comercial"},
    "AEROPORTO_HLZ":         {"lat": -27.6700, "lon": -48.5470, "perfil": "Aeroporto / logística"},
    "CAMPECHE":              {"lat": -27.6800, "lon": -48.4800, "perfil": "Expansão sul"},
    "LAGOA_CONCEICAO":       {"lat": -27.6050, "lon": -48.4600, "perfil": "Turismo / lazer"},
    "JURERE":                {"lat": -27.4400, "lon": -48.5000, "perfil": "Alto padrão balnear"},
    "CANASVIEIRAS":          {"lat": -27.4250, "lon": -48.4700, "perfil": "Turismo de massa"},
    "INGLESES":              {"lat": -27.4350, "lon": -48.3950, "perfil": "Residencial norte"},
    "NORTE_ILHA":            {"lat": -27.4800, "lon": -48.4500, "perfil": "Expansão norte"},
    "RESIDENCIAL_NORTE":     {"lat": -27.5420, "lon": -48.5000, "perfil": "Residencial expansão"},
    "SC401_CORREDOR":        {"lat": -27.5600, "lon": -48.5180, "perfil": "Corredor SC-401"},
    "SAO_JOSE_CENTRO":       {"lat": -27.6100, "lon": -48.6180, "perfil": "Centro de São José"},
    "SAO_JOSE_BARREIROS":    {"lat": -27.6450, "lon": -48.6500, "perfil": "Residencial sul SJ"},
    "SAO_JOSE_KOBRASOL":     {"lat": -27.5950, "lon": -48.6300, "perfil": "Comércio SJ"},
    "SAO_JOSE_ROCADO":       {"lat": -27.5700, "lon": -48.6500, "perfil": "Industrial SJ"},
    "PALHOCA_CENTRO":        {"lat": -27.6450, "lon": -48.6700, "perfil": "Centro de Palhoça"},
    "PALHOCA_PEDRA_BRANCA":  {"lat": -27.6250, "lon": -48.6900, "perfil": "Expansão Palhoça"},
    "PALHOCA_BR101_SUL":     {"lat": -27.6800, "lon": -48.7000, "perfil": "Corredor BR-101 Sul"},
    "BIGUACU_BR101_NORTE":   {"lat": -27.4950, "lon": -48.6550, "perfil": "Corredor BR-101 Norte"},
    "VIA_EXPRESSA_CORREDOR": {"lat": -27.6200, "lon": -48.5800, "perfil": "Via Expressa"},
    "SANTO_AMARO":           {"lat": -27.7100, "lon": -48.7800, "perfil": "Interior sul"},
    "GOV_CELSO_RAMOS":       {"lat": -27.3200, "lon": -48.5550, "perfil": "Litoral norte"},
    "ANTONIO_CARLOS":        {"lat": -27.5300, "lon": -48.7400, "perfil": "Hortigranjeiro / rural"},
}


@router.get("/mapa", response_model=MapaResponse)
async def obter_dados_mapa(
    indicador: Optional[str] = Query(
        None,
        description="Filtro por indicador (ex: n_usuarios, congestionamento_medio, drop_pct_medio).",
    )
):
    """
    Retorna coordenadas geográficas e indicadores consolidados de todos os
    27 clusters para renderização no mapa interativo Leaflet do frontend.
    Dados reais do dataset Vísent (tensor_concentracao.csv).
    """
    todos = _carregar_concentracao()
    agrupados = _agregar_por_cluster(list(todos))

    # Ordenação por indicador
    if indicador == "n_usuarios":
        agrupados.sort(key=lambda x: x["n_usuarios"], reverse=True)
    elif indicador == "congestionamento_medio":
        agrupados.sort(key=lambda x: x["congestionamento_medio"], reverse=True)
    elif indicador == "drop_pct_medio":
        agrupados.sort(key=lambda x: x["drop_pct_medio"], reverse=True)

    regioes = []
    for i, d in enumerate(agrupados):
        cluster_info = _CLUSTER_COORDS.get(d["cluster"], {})
        regioes.append(
            RegionMapData(
                id=i + 1,
                nome_cluster=d["cluster"],
                municipio=d["municipio"],
                latitude=cluster_info.get("lat", d["lat"]),
                longitude=cluster_info.get("lon", d["lon"]),
                perfil=cluster_info.get("perfil", "N/A"),
                n_usuarios=d["n_usuarios"],
                congestionamento_medio=d["congestionamento_medio"],
                cobertura_sinal_dbm=round(-80 - (d["drop_pct_medio"] * 100), 2),
            )
        )

    logger.info("GET /mapa: %d clusters retornados.", len(regioes))
    return MapaResponse(regioes=regioes)
