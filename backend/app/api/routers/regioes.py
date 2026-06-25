"""
Router de suporte: listagem de regiões/clusters para filtros do frontend.
Responsável: Willfredy (esqueleto inicial) — dados reais: Domingos.
"""

from fastapi import APIRouter
from app.models.schemas import RegioesResponse, RegionSimple

router = APIRouter()

# Dados mock iniciais — serão substituídos pelo repositório real (Domingos)
_MOCK_REGIOES = [
    RegionSimple(id=1, nome_cluster="Cazenga_1", municipio="Cazenga"),
    RegionSimple(id=2, nome_cluster="Viana_Centro", municipio="Viana"),
    RegionSimple(id=3, nome_cluster="Luanda_Norte", municipio="Luanda"),
    RegionSimple(id=4, nome_cluster="Cacuaco_1", municipio="Cacuaco"),
    RegionSimple(id=5, nome_cluster="Belas_Sul", municipio="Belas"),
]


@router.get("/regioes", response_model=RegioesResponse)
async def listar_regioes():
    """
    Retorna a listagem simplificada de todas as regiões/clusters disponíveis.
    Utilizada pelo frontend para preencher seletores e filtros.
    """
    return RegioesResponse(regioes=_MOCK_REGIOES)
