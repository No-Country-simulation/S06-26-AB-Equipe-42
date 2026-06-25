from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class QueryFilters(BaseModel):
    municipio: Optional[str] = Field(None, description="Nome do município para filtrar os dados.")
    periodo: Optional[str] = Field(None, description="Período do dia (ex: manha, tarde, noite).")

class QueryRequest(BaseModel):
    consulta: str = Field(..., description="Pergunta em linguagem natural sobre os dados.")
    filtros: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Filtros estruturados opcionais.")
    idioma: Optional[str] = Field("pt", description="Idioma da resposta gerada pela IA.")

    @field_validator('consulta')
    @classmethod
    def consulta_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("A consulta em linguagem natural não pode estar vazia.")
        return v.strip()

class SourceInfo(BaseModel):
    tabela: str = Field(..., description="Nome da tabela de origem dos dados.")
    descricao: str = Field(..., description="Breve descrição da fonte ou contexto do dado.")

class QueryResponse(BaseModel):
    resposta_ia: str = Field(..., description="Síntese textual em linguagem natural gerada pela IA.")
    dados: List[Dict[str, Any]] = Field(..., description="Lista de registos brutos recuperados da base de dados.")
    fontes: List[SourceInfo] = Field(..., description="Lista de fontes utilizadas para responder à consulta.")

class RegionMapData(BaseModel):
    id: int = Field(..., description="Identificador único da região/cluster.")
    nome_cluster: str = Field(..., description="Nome identificador do cluster.")
    municipio: str = Field(..., description="Município associado à região.")
    latitude: float = Field(..., description="Coordenada de latitude para o mapa.")
    longitude: float = Field(..., description="Coordenada de longitude para o mapa.")
    perfil: str = Field(..., description="Perfil demográfico ou de uso da região.")
    n_usuarios: int = Field(..., description="Volume de utilizadores ativos na região.")
    congestionamento_medio: float = Field(..., description="Taxa de congestionamento médio (0.0 a 1.0).")
    cobertura_sinal_dbm: float = Field(..., description="Qualidade média da cobertura de sinal em dBm.")

class MapaResponse(BaseModel):
    regioes: List[RegionMapData] = Field(..., description="Lista de regiões e seus indicadores consolidados para o mapa.")

class RegionSimple(BaseModel):
    id: int = Field(..., description="Identificador único da região/cluster.")
    nome_cluster: str = Field(..., description="Nome identificador do cluster.")
    municipio: str = Field(..., description="Município associado à região.")

class RegioesResponse(BaseModel):
    regioes: List[RegionSimple] = Field(..., description="Lista de todas as regiões para filtros do frontend.")

class IndicatorMetadata(BaseModel):
    id: str = Field(..., description="Identificador curto do indicador (ex: n_usuarios).")
    nome: str = Field(..., description="Nome amigável para exibição no frontend.")
    descricao: str = Field(..., description="Explicação detalhada do significado do indicador.")

class IndicadoresResponse(BaseModel):
    indicadores: List[IndicatorMetadata] = Field(..., description="Lista de indicadores suportados pela plataforma.")

class ServiceStatus(BaseModel):
    database: str = Field(..., description="Estado da ligação à base de dados (ex: connected, disconnected).")
    llm: str = Field(..., description="Estado do serviço de IA (ex: available, unavailable).")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Estado geral da API (ex: healthy, unhealthy).")
    timestamp: datetime = Field(..., default_factory=datetime.utcnow, description="Data e hora do diagnóstico.")
    services: ServiceStatus = Field(..., description="Estado individual de cada serviço de suporte.")
