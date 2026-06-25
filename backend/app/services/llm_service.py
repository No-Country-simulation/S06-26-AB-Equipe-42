"""
Serviço de Inteligência Artificial — Integração via OpenRouter.
Implementa o pipeline de interpretação e síntese da consulta em linguagem natural.

Integração: OpenAI SDK (cliente gratuito) apontando para OpenRouter.
Modelos gratuitos: google/gemini-2.5-flash:free ou meta-llama/llama-3-8b-instruct:free

Responsável: Edivaldo Bernardo (implementação real dos prompts e lógica LLM).
             Willfredy Vieira Dias (esqueleto de integração e contratos).
"""

import json
import logging
from typing import Optional

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

# Cliente OpenAI configurado para usar o OpenRouter (plano gratuito)
_client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY or "sem-chave-configurada",
    base_url=settings.OPENROUTER_BASE_URL,
)


async def interpretar_consulta(texto: str, idioma: str = "pt") -> dict:
    """
    Interpreta uma consulta em linguagem natural e extrai parâmetros estruturados.

    Usa function calling / JSON mode para extrair de forma fiável:
    - regiao: região ou município referenciado
    - indicador: métrica de interesse (ex: congestionamento, cobertura)
    - periodo: período do dia (manha, tarde, noite) se mencionado

    Args:
        texto: Pergunta em linguagem natural do utilizador.
        idioma: Idioma da resposta ('pt', 'en', 'es').

    Returns:
        Dicionário com os parâmetros extraídos: { regiao, indicador, periodo, confianca }.
    """
    if not settings.OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY não configurada — a usar interpretação mock.")
        return _interpretar_mock(texto)

    try:
        # Lê o template do ficheiro de prompts (responsabilidade do Edivaldo)
        prompt_sistema = _carregar_prompt("interpretar")

        resposta = await _client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"[idioma: {idioma}] {texto}"},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,  # Baixa criatividade para extração precisa
        )

        conteudo = resposta.choices[0].message.content
        resultado = json.loads(conteudo)
        logger.info("Consulta interpretada com sucesso: %s", resultado)
        return resultado

    except Exception as e:
        logger.error("Erro ao interpretar consulta via LLM: %s", str(e))
        # Fallback: devolve estrutura vazia com flag de baixa confiança
        return {"regiao": None, "indicador": None, "periodo": None, "confianca": 0.0}


async def sintetizar_resposta(
    dados: list,
    pergunta_original: str,
    idioma: str = "pt",
) -> str:
    """
    Sintetiza uma resposta em linguagem natural a partir dos dados reais da base de dados.

    REGRA CRÍTICA: A IA nunca inventa números.
    Apenas cita valores presentes nos dados fornecidos,
    com referências explícitas à fonte de cada valor.

    Args:
        dados: Lista de registos reais recuperados da base de dados.
        pergunta_original: Pergunta original do utilizador.
        idioma: Idioma da resposta ('pt', 'en', 'es').

    Returns:
        Texto em linguagem natural com a resposta sintetizada e fontes citadas.
    """
    if not settings.OPENROUTER_API_KEY or not dados:
        logger.warning("OPENROUTER_API_KEY não configurada ou dados vazios — a usar síntese mock.")
        return _sintetizar_mock(dados, pergunta_original)

    try:
        prompt_sistema = _carregar_prompt("sintetizar")
        dados_str = json.dumps(dados, ensure_ascii=False, indent=2)

        resposta = await _client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {
                    "role": "user",
                    "content": (
                        f"Pergunta original: {pergunta_original}\n"
                        f"Idioma da resposta: {idioma}\n\n"
                        f"Dados da base de dados:\n{dados_str}"
                    ),
                },
            ],
            temperature=0.3,
        )

        sintese = resposta.choices[0].message.content
        logger.info("Síntese gerada com sucesso (%d caracteres).", len(sintese))
        return sintese

    except Exception as e:
        logger.error("Erro ao sintetizar resposta via LLM: %s", str(e))
        # Degradação graciosa: usa síntese mock informativa com dados reais
        return _sintetizar_mock(dados, pergunta_original)


# ---------------------------------------------------------------------------
# Funções auxiliares privadas
# ---------------------------------------------------------------------------

def _carregar_prompt(nome: str) -> str:
    """
    Carrega o template de prompt a partir do ficheiro correspondente.
    Os prompts são versionados em ficheiros separados (não no código).
    """
    import os
    caminho = os.path.join(
        os.path.dirname(__file__), "prompts", f"{nome}.txt"
    )
    try:
        with open(caminho, encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.warning("Ficheiro de prompt '%s.txt' não encontrado. A usar prompt padrão.", nome)
        return _prompt_padrao(nome)


def _prompt_padrao(nome: str) -> str:
    """Prompts de fallback caso os ficheiros .txt ainda não existam."""
    if nome == "interpretar":
        return (
            "És um assistente especializado em análise de dados de rede móvel em Angola. "
            "Extrai do texto do utilizador os parâmetros: regiao, indicador, periodo e confianca (0.0 a 1.0). "
            "Responde SEMPRE em formato JSON válido com esses 4 campos."
        )
    if nome == "sintetizar":
        return (
            "És um assistente especializado em dados de rede móvel em Angola. "
            "Usa APENAS os dados fornecidos para responder. "
            "NUNCA inventes números. Cita os valores exactos dos dados. "
            "Responde no idioma indicado."
        )
    return "És um assistente útil."


def _interpretar_mock(texto: str) -> dict:
    """
    Interpretação heurística para quando o LLM não está disponível.
    Detecta palavras-chave de indicador, região, período e direção (maior/menor).
    """
    t = texto.lower()

    # --- Indicador ---
    indicador = None
    if any(p in t for p in ["congest", "saturad", "tráfego", "trafego"]):
        indicador = "congestionamento_medio"
    elif any(p in t for p in ["utilizador", "usuario", "pessoas", "população", "populacao"]):
        indicador = "n_usuarios"
    elif any(p in t for p in ["sinal", "cobertura", "dbm", "qualidade"]):
        indicador = "drop_pct_medio"

    # --- Período ---
    periodo = None
    if any(p in t for p in ["manhã", "manha", "manhã"]):
        periodo = "MANHA"
    elif "tarde" in t:
        periodo = "TARDE"
    elif "noite" in t:
        periodo = "NOITE"
    elif "madrugada" in t:
        periodo = "MADRUGADA"

    # --- Região ---
    regiao = None
    regioes_conhecidas = [
        "beiramar", "beira-mar", "trindade", "ufsc", "coqueiros",
        "estreito", "aeroporto", "campeche", "lagoa", "jurere",
        "canasvieiras", "ingleses", "norte", "kobrasol", "palhoca",
        "biguacu", "sao jose", "são josé", "via expressa",
        "florianopolis", "florianópolis",
    ]
    for r in regioes_conhecidas:
        if r in t:
            regiao = r
            break

    # --- Direção: menor/pior → ordem crescente ---
    ordem_crescente = any(p in t for p in ["menor", "mínimo", "minimo", "pior", "menos", "baixo", "baixa"])

    return {
        "regiao": regiao,
        "indicador": indicador or "congestionamento_medio",
        "periodo": periodo,
        "ordem_crescente": ordem_crescente,
        "confianca": 0.5,
        "mock": True,
    }


def _sintetizar_mock(dados: list, pergunta: str) -> str:
    """
    Síntese automática com base nos dados reais quando o LLM não está disponível.
    Usa os campos reais devolvidos pelo data_service (cluster, municipio, etc.).
    """
    if not dados:
        return "Não foram encontrados dados para a sua consulta."

    top = dados[0]
    cluster = top.get("cluster", "desconhecido")
    municipio = top.get("municipio", "município desconhecido")
    n_usuarios = top.get("n_usuarios", 0)
    congestionamento = top.get("congestionamento_medio", 0)
    drop = top.get("drop_pct_medio", 0)

    linhas = [
        f"Com base nos dados do dataset Vísent (tensor_concentracao), "
        f"o cluster com maior destaque para a sua consulta é **{cluster}** "
        f"(município de {municipio}).",
        f"\nIndicadores agregados: {n_usuarios:,} utilizadores ativos, "
        f"congestionamento médio de {congestionamento:.1%}, "
        f"taxa de descarte de pacotes de {drop:.1%}.",
    ]

    if len(dados) > 1:
        segundo = dados[1]
        linhas.append(
            f"\nO segundo cluster é **{segundo.get('cluster', '—')}** "
            f"({segundo.get('municipio', '—')}) com "
            f"{segundo.get('n_usuarios', 0):,} utilizadores."
        )

    linhas.append(
        f"\n\nFonte: tensor_concentracao — Dataset Vísent CDRView AppBiT v2 "
        f"(Visent / OSX Telecomunicações S/A, jun/2026)."
    )
    return "".join(linhas)
