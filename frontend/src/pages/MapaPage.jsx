import React, { useState } from 'react';
import { useMapaData, useIndicadores } from '../hooks/useDados.js';
import MapaRegioes from '../components/MapaRegioes.jsx';
import { Filter, Layers, Info, Users, Activity, Signal, AlertCircle } from 'lucide-react';

function MapaPage() {
  const [selectedIndicator, setSelectedIndicator] = useState('n_usuarios');

  const { data: indicatorsData, isLoading: isLoadingIndicators } = useIndicadores();
  const { data: mapData, isLoading: isLoadingMap, isError, error } = useMapaData(selectedIndicator);

  const getIndicatorIcon = (id) => {
    switch (id) {
      case 'n_usuarios':
        return <Users size={16} />;
      case 'congestionamento_medio':
        return <Activity size={16} />;
      case 'cobertura_sinal_dbm':
        return <Signal size={16} />;
      default:
        return <Layers size={16} />;
    }
  };

  const currentIndicator = indicatorsData?.indicadores?.find(ind => ind.id === selectedIndicator);

  return (
    <div className="page-container mapa-page">
      <div className="page-header">
        <h1 className="page-title">Mapa Interativo</h1>
        <p className="page-subtitle">
          Visualização espacial dos 27 clusters regionais. Selecione um indicador para analisar o desempenho de rede.
        </p>
      </div>

      <div className="mapa-layout">
        <div className="mapa-controls glass-panel">
          <div className="controls-section-header">
            <Filter size={18} />
            <h3>Indicador de Análise</h3>
          </div>

          <div className="indicators-selector">
            {isLoadingIndicators ? (
              <div className="loading-indicators">Carregando indicadores...</div>
            ) : (
              indicatorsData?.indicadores?.map((ind) => (
                <button
                  key={ind.id}
                  onClick={() => setSelectedIndicator(ind.id)}
                  className={`indicator-btn ${selectedIndicator === ind.id ? 'active' : ''}`}
                >
                  <span className="btn-icon">{getIndicatorIcon(ind.id)}</span>
                  <div className="btn-details">
                    <span className="btn-name">{ind.nome}</span>
                    <span className="btn-desc-brief">{ind.descricao.split('.')[0]}.</span>
                  </div>
                </button>
              ))
            )}
          </div>

          {currentIndicator && (
            <div className="indicator-info-panel">
              <div className="info-title">
                <Info size={14} color="var(--accent-cyan)" />
                <span>Sobre o Indicador</span>
              </div>
              <p className="info-desc">{currentIndicator.descricao}</p>
            </div>
          )}

          <div className="legend-panel">
            <h4 className="legend-title">Legenda</h4>
            
            {selectedIndicator === 'n_usuarios' && (
              <div className="legend-list">
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: '#22d3ee' }}></span>
                  <span>Baixa Densidade (&lt; 200 utilizadores)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: 'var(--accent-cyan)' }}></span>
                  <span>Média Densidade (200 - 800 utilizadores)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: '#3b82f6' }}></span>
                  <span>Alta Densidade (&gt; 800 utilizadores)</span>
                </div>
                <div className="legend-note">*O tamanho dos marcadores reflete proporcionalmente o volume de utilizadores.</div>
              </div>
            )}

            {selectedIndicator === 'congestionamento_medio' && (
              <div className="legend-list">
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: 'var(--color-success)' }}></span>
                  <span>Fluido (&lt; 30% congestionamento)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: 'var(--color-warning)' }}></span>
                  <span>Moderado (30% - 60% congestionamento)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: 'var(--color-danger)' }}></span>
                  <span>Congestionado (&gt; 60% congestionamento)</span>
                </div>
              </div>
            )}

            {selectedIndicator === 'cobertura_sinal_dbm' && (
              <div className="legend-list">
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: 'var(--color-success)' }}></span>
                  <span>Sinal Forte (&ge; -90 dBm)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: 'var(--color-warning)' }}></span>
                  <span>Sinal Médio (-90 a -105 dBm)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot" style={{ backgroundColor: 'var(--color-danger)' }}></span>
                  <span>Sinal Fraco (&lt; -105 dBm)</span>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="mapa-wrapper glass-panel">
          {isLoadingMap ? (
            <div className="map-loading-container">
              <span className="spinner" style={{ width: '32px', height: '32px', borderWidth: '3px' }}></span>
              <h3>Carregando Mapa de Redes...</h3>
              <p>Obtendo coordenadas geográficas e agregando dados dos clusters...</p>
            </div>
          ) : isError ? (
            <div className="map-error-container">
              <AlertCircle size={32} color="var(--color-danger)" />
              <h3>Falha ao Carregar o Mapa</h3>
              <p>{error?.response?.data?.detail || "Erro ao conectar à API. Certifique-se de que o backend está ativo."}</p>
            </div>
          ) : (
            mapData?.regioes && (
              <MapaRegioes 
                regions={mapData.regioes} 
                selectedIndicator={selectedIndicator} 
              />
            )
          )}
        </div>
      </div>
    </div>
  );
}

export default MapaPage;
