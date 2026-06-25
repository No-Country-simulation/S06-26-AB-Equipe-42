"""
Ponto de entrada principal da aplicação FastAPI.
Inicializa a app, configura CORS e regista todos os routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routers import health, dados, mapa, regioes, indicadores

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API do AppBit Painel — plataforma de consulta inteligente de dados de rede e mobilidade de Angola.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Configuração de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registo dos Routers ---
app.include_router(health.router, tags=["Monitorização"])
app.include_router(dados.router, tags=["Consulta Inteligente"])
app.include_router(mapa.router, tags=["Mapa Interativo"])
app.include_router(regioes.router, tags=["Regiões"])
app.include_router(indicadores.router, tags=["Indicadores"])


@app.get("/", include_in_schema=False)
async def root():
    """Redireciona para a documentação interativa da API."""
    return {
        "mensagem": f"Bem-vindo à {settings.APP_NAME}",
        "versao": settings.APP_VERSION,
        "documentacao": "/docs",
    }
