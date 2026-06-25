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
    LLM_MODEL: str = os.getenv("LLM_MODEL", "google/gemini-2.5-flash:free")

    # --- CORS ---
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")


settings = Settings()
