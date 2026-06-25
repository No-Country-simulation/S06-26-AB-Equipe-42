"""
Endpoint de verificação de saúde da API.
Permite ao frontend e ao sistema de CI/CD verificar
se o backend e os seus serviços dependentes estão operacionais.
"""

from datetime import datetime, timezone
from fastapi import APIRouter

from app.models.schemas import HealthResponse, ServiceStatus

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Verifica o estado operacional da API e das dependências externas.
    Retorna o estado da ligação à base de dados e ao serviço de IA.
    """
    # TODO: Implementar verificação real da base de dados (Domingos)
    db_status = "connected"

    # TODO: Implementar verificação real do serviço LLM (Edivaldo)
    llm_status = "available"

    overall = "healthy" if db_status == "connected" and llm_status == "available" else "unhealthy"

    return HealthResponse(
        status=overall,
        timestamp=datetime.now(timezone.utc),
        services=ServiceStatus(
            database=db_status,
            llm=llm_status,
        ),
    )
