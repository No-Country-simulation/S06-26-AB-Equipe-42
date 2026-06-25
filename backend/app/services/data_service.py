"""
Serviço de Dados — Orquestração entre repositórios e serviço LLM.
Carrega dados reais do dataset Vísent (tensor_concentracao.csv) de forma eficiente.
Responsável: Willfredy Vieira Dias.

Dataset utilizado: tensor_concentracao.csv (1.1 MB — carregamento completo em memória)
Fonte: CDRView AppBiT Technical Reference v2 — Visent / OSX Telecomunicações S/A
"""

import csv
import logging
import os
from functools import lru_cache
from typing import Any

from app.models.schemas import SourceInfo

logger = logging.getLogger(__name__)

# Caminho para o dataset — usa data/raw/ (versionado no git)
def _encontrar_repo_root() -> str:
    """
    Encontra a raiz do repositório verificando onde data/raw/ está.
    Suporta execução a partir da raiz do repo ou da pasta backend/.
    """
    cwd = os.getcwd()
    # Tentativa 1: CWD é a raiz do repo (data/raw/ existe aqui)
    if os.path.isdir(os.path.join(cwd, "data", "raw")):
        return cwd
    # Tentativa 2: CWD é backend/ — sobe 1 nível
    parent = os.path.abspath(os.path.join(cwd, ".."))
    if os.path.isdir(os.path.join(parent, "data", "raw")):
        return parent
    # Tentativa 3: sobe 4 níveis a partir deste ficheiro (app/services/)
    file_candidate = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
    )
    if os.path.isdir(os.path.join(file_candidate, "data", "raw")):
        return file_candidate
    # Fallback: CWD
    return cwd


_REPO_ROOT = _encontrar_repo_root()
# data/raw/ contém os CSVs pequenos versionados no git.
# Os ficheiros grandes (tensor_mobilidade.csv, tensor_sequencias.csv)
# devem ser descarregados manualmente — ver data/raw/README.md
_DATASET_PATH = os.path.join(_REPO_ROOT, "data", "raw", "tensor_concentracao.csv")


@lru_cache(maxsize=1)
def _carregar_concentracao() -> list[dict]:
    """
    Carrega o tensor_concentracao.csv em memória uma única vez (cache LRU).
    Ficheiro pequeno (1.1 MB) — adequado para carregamento completo.

    CRÍTICO: ecgi é sempre lido como STRING (nunca como número).
    """
    caminho = os.path.abspath(_DATASET_PATH)
    if not os.path.exists(caminho):
        logger.warning(
            "tensor_concentracao.csv não encontrado em '%s'. A usar dados mock de fallback.", caminho
        )
        return _fallback_mock()

    dados = []
    try:
        with open(caminho, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dados.append({
                    "ecgi": str(row["ecgi"]),           # CRÍTICO: sempre string
                    "cluster": row["cluster"],
                    "municipio": row["municipio"],
                    "day_date": row["day_date"],
                    "periodo": row["periodo"],
                    "n_usuarios": int(row["n_usuarios"]),
                    "n_sessoes": int(row["n_sessoes"]),
                    "download_bytes": int(row["download_bytes"]),
                    "upload_bytes": int(row["upload_bytes"]),
                    "dur_media_s": int(row["dur_media_s"]),
                    "drop_pct_medio": float(row["drop_pct_medio"]),
                    "congestionamento_medio": float(row["congestionamento_medio"]),
                    "chamadas_total": int(row["chamadas_total"]),
                    "mensagens_total": int(row["mensagens_total"]),
                    "lat": float(row["lat"]),
                    "lon": float(row["lon"]),
                })
        logger.info("tensor_concentracao.csv carregado: %d registos.", len(dados))
    except Exception as e:
        logger.error("Erro ao carregar tensor_concentracao.csv: %s", str(e))
        return _fallback_mock()

    return dados


async def pesquisar_dados(parametros: dict[str, Any]) -> tuple[list[dict], list[SourceInfo]]:
    """
    Pesquisa os dados relevantes no tensor_concentracao.csv com base nos
    parâmetros extraídos pelo serviço LLM (regiao, indicador, periodo).

    Args:
        parametros: Dicionário com { regiao, indicador, periodo, confianca }.

    Returns:
        Tuplo (dados, fontes) com os registos filtrados e as fontes utilizadas.
    """
    regiao_filtro: str | None = parametros.get("regiao")
    indicador: str | None = parametros.get("indicador")
    periodo_filtro: str | None = parametros.get("periodo")

    todos_os_dados = _carregar_concentracao()
    dados = list(todos_os_dados)  # cópia para não alterar o cache

    # --- Filtro por região/município/cluster ---
    if regiao_filtro:
        regiao_lower = regiao_filtro.lower()
        dados = [
            d for d in dados
            if regiao_lower in d["municipio"].lower()
            or regiao_lower in d["cluster"].lower()
        ]
        logger.info("Filtro de região '%s': %d resultado(s).", regiao_filtro, len(dados))

    # --- Filtro por período do dia ---
    if periodo_filtro:
        periodo_upper = periodo_filtro.upper()
        dados = [d for d in dados if d["periodo"] == periodo_upper]
        logger.info("Filtro de período '%s': %d resultado(s).", periodo_filtro, len(dados))

    # --- Agrupamento por cluster (média dos indicadores) ---
    dados_agrupados = _agregar_por_cluster(dados)

    # --- Ordenação pelo indicador de interesse ---
    if indicador == "n_usuarios":
        dados_agrupados.sort(key=lambda x: x["n_usuarios"], reverse=True)
    elif indicador == "congestionamento_medio":
        dados_agrupados.sort(key=lambda x: x["congestionamento_medio"], reverse=True)
    elif indicador == "drop_pct_medio":
        dados_agrupados.sort(key=lambda x: x["drop_pct_medio"], reverse=True)
    else:
        # Sem indicador específico: ordena por número de utilizadores
        dados_agrupados.sort(key=lambda x: x["n_usuarios"], reverse=True)

    fontes = [
        SourceInfo(
            tabela="tensor_concentracao",
            descricao="Dataset Vísent — CDRView AppBiT v2 (Visent / OSX Telecomunicações S/A). "
                      "Dados sintéticos de 200K assinantes, 132 ERBs, 27 clusters — RM de Florianópolis.",
        )
    ]

    return dados_agrupados[:10], fontes  # Limite de 10 registos por resposta


def _agregar_por_cluster(dados: list[dict]) -> list[dict]:
    """
    Agrega os dados por cluster, calculando a média dos indicadores numéricos
    e a soma dos contadores (n_usuarios, chamadas, etc.).
    """
    clusters: dict[str, dict] = {}
    for d in dados:
        chave = d["cluster"]
        if chave not in clusters:
            clusters[chave] = {
                "cluster": d["cluster"],
                "municipio": d["municipio"],
                "lat": d["lat"],
                "lon": d["lon"],
                "n_usuarios": 0,
                "n_sessoes": 0,
                "congestionamento_medio": [],
                "drop_pct_medio": [],
                "chamadas_total": 0,
                "mensagens_total": 0,
                "_count": 0,
            }
        c = clusters[chave]
        c["n_usuarios"] += d["n_usuarios"]
        c["n_sessoes"] += d["n_sessoes"]
        c["congestionamento_medio"].append(d["congestionamento_medio"])
        c["drop_pct_medio"].append(d["drop_pct_medio"])
        c["chamadas_total"] += d["chamadas_total"]
        c["mensagens_total"] += d["mensagens_total"]
        c["_count"] += 1

    # Calcular médias
    resultado = []
    for c in clusters.values():
        count = c["_count"] or 1
        resultado.append({
            "cluster": c["cluster"],
            "municipio": c["municipio"],
            "lat": c["lat"],
            "lon": c["lon"],
            "n_usuarios": c["n_usuarios"],
            "n_sessoes": c["n_sessoes"],
            "congestionamento_medio": round(sum(c["congestionamento_medio"]) / count, 4),
            "drop_pct_medio": round(sum(c["drop_pct_medio"]) / count, 4),
            "chamadas_total": c["chamadas_total"],
            "mensagens_total": c["mensagens_total"],
        })

    return resultado


def _fallback_mock() -> list[dict]:
    """Dados de fallback caso o CSV não esteja disponível."""
    return [
        {
            "ecgi": "000000000001",
            "cluster": "CBD_BEIRAMAR",
            "municipio": "Florianopolis",
            "day_date": "2026-03-01",
            "periodo": "MANHA",
            "n_usuarios": 1367,
            "n_sessoes": 5538,
            "download_bytes": 104305839720,
            "upload_bytes": 15731146936,
            "dur_media_s": 469,
            "drop_pct_medio": 0.0668,
            "congestionamento_medio": 0.348,
            "chamadas_total": 3930,
            "mensagens_total": 3025,
            "lat": -27.585,
            "lon": -48.544722,
        },
    ]
