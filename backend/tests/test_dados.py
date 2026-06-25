"""
Testes unitários para o endpoint POST /dados.
Responsável: Willfredy Vieira Dias.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Testes de sucesso
# ---------------------------------------------------------------------------

def test_dados_consulta_simples():
    """Deve retornar 200 com resposta_ia, dados e fontes para uma consulta válida."""
    resposta = client.post("/dados", json={
        "consulta": "Qual o cluster com maior congestionamento?",
        "filtros": {},
        "idioma": "pt"
    })
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert "resposta_ia" in corpo
    assert "dados" in corpo
    assert "fontes" in corpo
    assert isinstance(corpo["dados"], list)
    assert isinstance(corpo["fontes"], list)
    assert len(corpo["dados"]) > 0


def test_dados_consulta_com_filtro_regiao():
    """Deve filtrar resultados por região/município quando especificado."""
    resposta = client.post("/dados", json={
        "consulta": "Dados de Florianopolis",
        "filtros": {"regiao": "Florianopolis"},
        "idioma": "pt"
    })
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["dados"]) > 0
    # Todos os registos devem ser de Florianopolis
    for dado in corpo["dados"]:
        assert "Florianopolis" in dado.get("municipio", "") or \
               "Florianopolis" in dado.get("cluster", "")


def test_dados_consulta_sem_filtros():
    """Deve funcionar sem filtros opcionais."""
    resposta = client.post("/dados", json={
        "consulta": "Mostre os dados de utilizadores"
    })
    assert resposta.status_code == 200
    assert "resposta_ia" in resposta.json()


def test_dados_resposta_tem_fonte_dataset_visent():
    """A fonte dos dados deve referenciar o dataset Vísent."""
    resposta = client.post("/dados", json={
        "consulta": "Quais as antenas com mais utilizadores?"
    })
    assert resposta.status_code == 200
    fontes = resposta.json()["fontes"]
    assert any("tensor_concentracao" in f["tabela"] for f in fontes)


def test_dados_resposta_campos_numericos_validos():
    """Os dados retornados devem ter campos numéricos válidos."""
    resposta = client.post("/dados", json={
        "consulta": "Dados de congestionamento"
    })
    assert resposta.status_code == 200
    dados = resposta.json()["dados"]
    for d in dados:
        if "n_usuarios" in d:
            assert isinstance(d["n_usuarios"], (int, float))
            assert d["n_usuarios"] >= 0
        if "congestionamento_medio" in d:
            assert 0.0 <= d["congestionamento_medio"] <= 1.0


# ---------------------------------------------------------------------------
# Testes de validação / erros esperados
# ---------------------------------------------------------------------------

def test_dados_consulta_vazia_retorna_422():
    """Consulta vazia deve ser rejeitada com erro de validação (422)."""
    resposta = client.post("/dados", json={
        "consulta": "",
        "filtros": {}
    })
    assert resposta.status_code == 422


def test_dados_consulta_apenas_espacos_retorna_422():
    """Consulta com apenas espaços deve ser rejeitada (422)."""
    resposta = client.post("/dados", json={
        "consulta": "   ",
    })
    assert resposta.status_code == 422


def test_dados_sem_corpo_retorna_422():
    """Pedido sem corpo JSON deve retornar erro de validação (422)."""
    resposta = client.post("/dados")
    assert resposta.status_code == 422


def test_dados_campo_consulta_obrigatorio():
    """O campo 'consulta' é obrigatório — sem ele deve retornar 422."""
    resposta = client.post("/dados", json={"filtros": {}})
    assert resposta.status_code == 422
