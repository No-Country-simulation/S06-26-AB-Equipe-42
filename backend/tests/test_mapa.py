"""
Testes unitários para o endpoint GET /mapa.
Responsável: Willfredy Vieira Dias.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Testes de sucesso
# ---------------------------------------------------------------------------

def test_mapa_retorna_200():
    """GET /mapa deve retornar 200 com lista de regiões."""
    resposta = client.get("/mapa")
    assert resposta.status_code == 200


def test_mapa_estrutura_resposta():
    """A resposta deve conter o campo 'regioes' como lista."""
    resposta = client.get("/mapa")
    corpo = resposta.json()
    assert "regioes" in corpo
    assert isinstance(corpo["regioes"], list)
    assert len(corpo["regioes"]) > 0


def test_mapa_campos_obrigatorios_por_regiao():
    """Cada região deve ter todos os campos obrigatórios definidos no schema."""
    resposta = client.get("/mapa")
    regioes = resposta.json()["regioes"]
    campos_obrigatorios = [
        "id", "nome_cluster", "municipio",
        "latitude", "longitude", "perfil",
        "n_usuarios", "congestionamento_medio", "cobertura_sinal_dbm"
    ]
    for regiao in regioes:
        for campo in campos_obrigatorios:
            assert campo in regiao, f"Campo '{campo}' em falta na região: {regiao.get('nome_cluster')}"


def test_mapa_coordenadas_validas():
    """As coordenadas de latitude e longitude devem estar em intervalos válidos."""
    resposta = client.get("/mapa")
    for r in resposta.json()["regioes"]:
        assert -90 <= r["latitude"] <= 90, f"Latitude inválida: {r['latitude']}"
        assert -180 <= r["longitude"] <= 180, f"Longitude inválida: {r['longitude']}"


def test_mapa_indicadores_em_intervalos_validos():
    """Os indicadores numéricos devem estar em intervalos coerentes."""
    resposta = client.get("/mapa")
    for r in resposta.json()["regioes"]:
        assert r["n_usuarios"] >= 0
        assert 0.0 <= r["congestionamento_medio"] <= 1.0
        assert r["cobertura_sinal_dbm"] < 0, "sinal dBm deve ser negativo"


def test_mapa_ids_unicos():
    """Cada região deve ter um ID único."""
    resposta = client.get("/mapa")
    ids = [r["id"] for r in resposta.json()["regioes"]]
    assert len(ids) == len(set(ids)), "IDs das regiões não são únicos"


def test_mapa_27_clusters_dataset_visent():
    """O dataset Vísent tem 27 clusters — o mapa deve retornar até 27 regiões."""
    resposta = client.get("/mapa")
    regioes = resposta.json()["regioes"]
    assert len(regioes) <= 27, f"Mais de 27 clusters retornados: {len(regioes)}"
    assert len(regioes) >= 1


# ---------------------------------------------------------------------------
# Testes com filtro por indicador
# ---------------------------------------------------------------------------

def test_mapa_com_filtro_indicador_n_usuarios():
    """Com indicador=n_usuarios, a ordenação deve ser decrescente por utilizadores."""
    resposta = client.get("/mapa?indicador=n_usuarios")
    assert resposta.status_code == 200
    regioes = resposta.json()["regioes"]
    if len(regioes) > 1:
        utilizadores = [r["n_usuarios"] for r in regioes]
        assert utilizadores == sorted(utilizadores, reverse=True), \
            "Regiões não estão ordenadas por n_usuarios decrescente"


def test_mapa_com_filtro_indicador_congestionamento():
    """Com indicador=congestionamento_medio, a ordenação deve ser decrescente."""
    resposta = client.get("/mapa?indicador=congestionamento_medio")
    assert resposta.status_code == 200
    regioes = resposta.json()["regioes"]
    if len(regioes) > 1:
        valores = [r["congestionamento_medio"] for r in regioes]
        assert valores == sorted(valores, reverse=True)


def test_mapa_com_indicador_invalido_ainda_retorna_200():
    """Um indicador desconhecido não deve causar erro — deve retornar 200 com ordem padrão."""
    resposta = client.get("/mapa?indicador=indicador_inexistente")
    assert resposta.status_code == 200


# ---------------------------------------------------------------------------
# Teste de saúde
# ---------------------------------------------------------------------------

def test_health_endpoint():
    """GET /health deve retornar estado healthy."""
    resposta = client.get("/health")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert "status" in corpo
    assert corpo["status"] in ("healthy", "unhealthy")
    assert "services" in corpo
    assert "timestamp" in corpo
