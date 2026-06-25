"""
Configurações centrais da aplicação.
Lê as variáveis de ambiente a partir de um ficheiro .env
e expõe-as como atributos tipados para o resto do backend.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configurações globais da aplicação AppBit Painel."""

    # --- Informações da Aplicação ---
    APP_NAME: str = "AppBit Painel API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # --- Base de Dados (Supabase / PostgreSQL) ---
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # --- Serviço de IA (OpenRouter — compatível com OpenAI SDK) ---
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = os.getenv(
        "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
    )
    # Modelos gratuitos confirmados no OpenRouter (jun/2026) — $0/M tokens:
    # openai/gpt-oss-120b:free       ← RECOMENDADO (suporte nativo a JSON + function calling)
    # google/gemma-4-31b-it:free     ← boa alternativa (multilíngue, bom em Português)
    # nvidia/nemotron-3-ultra:free   ← poderoso (550B MoE, 1M context)
    # openrouter/owl-alpha           ← agentic workflows
    # nvidia/nemotron-3-super:free   ← 120B, bom equilíbrio
    LLM_MODEL: str = os.getenv("LLM_MODEL", "openai/gpt-oss-120b:free")

    # --- CORS ---
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")


settings = Settings()
