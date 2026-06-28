import React, { useState, useEffect } from 'react';
import { useIntelligentQuery } from '../hooks/useDados.js';
import AiQueryBar from '../components/AiQueryBar.jsx';
import RespostaCard from '../components/RespostaCard.jsx';
import { History, Trash2, Filter, ChevronDown, ChevronUp, AlertCircle, HelpCircle } from 'lucide-react';

function ConsultaPage() {
  const [history, setHistory] = useState([]);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [selectedMunicipio, setSelectedMunicipio] = useState('');
  const [selectedPeriodo, setSelectedPeriodo] = useState('');

  const municipios = ["Luanda", "Viana", "Cazenga", "Cacuaco", "Belas"];
  const periodos = [
    { id: "manha", label: "Manhã" },
    { id: "tarde", label: "Tarde" },
    { id: "noite", label: "Noite" }
  ];

  const queryMutation = useIntelligentQuery();

  useEffect(() => {
    const savedHistory = localStorage.getItem('appbit_query_history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error(e);
      }
    }
  }, []);

  const saveHistory = (newHistory) => {
    setHistory(newHistory);
    localStorage.setItem('appbit_query_history', JSON.stringify(newHistory));
  };

  const handleQuerySubmit = (queryText) => {
    const activeFilters = {};
    if (selectedMunicipio) activeFilters.municipio = selectedMunicipio;
    if (selectedPeriodo) activeFilters.periodo = selectedPeriodo;

    queryMutation.mutate(
      { consulta: queryText, filtros: activeFilters },
      {
        onSuccess: (data) => {
          const newHistoryItem = {
            id: Date.now(),
            pergunta: queryText,
            timestamp: new Date().toLocaleTimeString('pt-PT', { hour: '2-digit', minute: '2-digit' }),
            filtros: activeFilters,
            response: data,
          };
          const filteredHistory = history.filter(item => item.pergunta.toLowerCase() !== queryText.toLowerCase());
          saveHistory([newHistoryItem, ...filteredHistory].slice(0, 5));
        },
      }
    );
  };

  const handleHistoryItemClick = (item) => {
    setSelectedMunicipio(item.filtros?.municipio || '');
    setSelectedPeriodo(item.filtros?.periodo || '');
    
    queryMutation.mutate({ consulta: item.pergunta, filtros: item.filtros });
  };

  const clearHistory = () => {
    saveHistory([]);
  };

  return (
    <div className="page-container consulta-page">
      <div className="page-header">
        <h1 className="page-title">Consulta Inteligente</h1>
        <p className="page-subtitle">
          Faça perguntas sobre cobertura de sinal, tráfego e qualidade de rede usando linguagem natural.
        </p>
      </div>

      <div className="consulta-layout">
        <div className="consulta-main">
          <div className="filters-accordion glass-panel">
            <button 
              className="filters-toggle-btn"
              onClick={() => setFiltersOpen(!filtersOpen)}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Filter size={16} color={selectedMunicipio || selectedPeriodo ? '#06b6d4' : 'currentColor'} />
                <span>Filtros Estruturados {selectedMunicipio || selectedPeriodo ? '(Ativos)' : ''}</span>
              </div>
              {filtersOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>

            {filtersOpen && (
              <div className="filters-body">
                <div className="filter-group">
                  <label htmlFor="municipio-select">Município:</label>
                  <select 
                    id="municipio-select"
                    value={selectedMunicipio}
                    onChange={(e) => setSelectedMunicipio(e.target.value)}
                    className="filter-select"
                  >
                    <option value="">Todos os Municípios</option>
                    {municipios.map(m => (
                      <option key={m} value={m}>{m}</option>
                    ))}
                  </select>
                </div>

                <div className="filter-group">
                  <label htmlFor="periodo-select">Período do Dia:</label>
                  <select 
                    id="periodo-select"
                    value={selectedPeriodo}
                    onChange={(e) => setSelectedPeriodo(e.target.value)}
                    className="filter-select"
                  >
                    <option value="">Todos os Períodos</option>
                    {periodos.map(p => (
                      <option key={p.id} value={p.id}>{p.label}</option>
                    ))}
                  </select>
                </div>

                {(selectedMunicipio || selectedPeriodo) && (
                  <button 
                    onClick={() => { setSelectedMunicipio(''); setSelectedPeriodo(''); }}
                    className="clear-filters-btn"
                  >
                    Limpar Filtros
                  </button>
                )}
              </div>
            )}
          </div>

          <AiQueryBar onSubmit={handleQuerySubmit} isLoading={queryMutation.isPending} />

          {queryMutation.isError && (
            <div className="error-message-container glass-panel">
              <AlertCircle size={20} className="error-icon" />
              <div>
                <h4>Ocorreu um erro no processamento</h4>
                <p>{queryMutation.error?.response?.data?.detail || "Impossível ligar ao servidor do AppBit. Certifique-se de que o backend está a correr."}</p>
              </div>
            </div>
          )}

          {queryMutation.isSuccess && (
            <RespostaCard response={queryMutation.data} />
          )}

          {!queryMutation.isPending && !queryMutation.isSuccess && !queryMutation.isError && (
            <div className="empty-state-container glass-panel">
              <HelpCircle size={40} className="help-icon" />
              <h3>Faça a sua primeira pergunta</h3>
              <p>
                Escreva a sua dúvida sobre tráfego móvel e dados de rede acima, ou clique numa das sugestões sugeridas para ver dados reais de cobertura da rede de Angola.
              </p>
            </div>
          )}

          {queryMutation.isPending && (
            <div className="loading-state-container glass-panel">
              <div className="loading-anim">
                <div className="circle-pulse"></div>
                <div className="circle-pulse delay-1"></div>
              </div>
              <h3>A consultar a Inteligência Artificial...</h3>
              <p>A interpretar pergunta, analisar tabelas do dataset Vísent e sintetizar resposta.</p>
            </div>
          )}
        </div>

        <div className="consulta-sidebar glass-panel">
          <div className="sidebar-section-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <History size={18} />
              <h3>Histórico Recente</h3>
            </div>
            {history.length > 0 && (
              <button 
                onClick={clearHistory} 
                className="btn-clear-history" 
                title="Limpar histórico"
                aria-label="Limpar histórico de consultas"
              >
                <Trash2 size={16} />
              </button>
            )}
          </div>

          {history.length === 0 ? (
            <div className="empty-history">
              <p>Nenhuma pergunta no histórico local.</p>
            </div>
          ) : (
            <ul className="history-list">
              {history.map((item) => (
                <li key={item.id} className="history-item">
                  <button onClick={() => handleHistoryItemClick(item)} className="history-item-btn">
                    <span className="history-item-text" title={item.pergunta}>{item.pergunta}</span>
                    <span className="history-item-time">{item.timestamp}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default ConsultaPage;
