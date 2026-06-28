import React, { useState } from 'react';
import { Database, FileText, ChevronDown, ChevronUp } from 'lucide-react';

function RespostaCard({ response }) {
  const [showRawData, setShowRawData] = useState(false);

  if (!response) return null;

  const { resposta_ia, dados, fontes } = response;
  const tableColumns = dados && dados.length > 0 ? Object.keys(dados[0]) : [];

  const formatHeader = (key) => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  return (
    <div className="resposta-card-container glass-panel">
      <div className="resposta-ia-section">
        <div className="resposta-section-header">
          <div className="ai-icon-pulse">
            <span className="pulse-dot"></span>
          </div>
          <h3>Resposta da IA</h3>
        </div>
        <div className="resposta-text">
          {resposta_ia.split('\n').map((paragraph, index) => (
            <p key={index} style={{ marginBottom: paragraph ? '12px' : '4px' }}>
              {paragraph}
            </p>
          ))}
        </div>
      </div>

      {fontes && fontes.length > 0 && (
        <div className="fontes-section">
          <div className="fontes-header">
            <FileText size={16} className="fontes-icon" />
            <span>Fontes Utilizadas:</span>
          </div>
          <div className="fontes-list">
            {fontes.map((fonte, idx) => (
              <div key={idx} className="fonte-badge" title={fonte.descricao}>
                <span className="fonte-table">{fonte.tabela}</span>
                <span className="fonte-desc">{fonte.descricao}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {dados && dados.length > 0 && (
        <div className="raw-data-accordion">
          <button 
            className="accordion-header-btn" 
            onClick={() => setShowRawData(!showRawData)}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Database size={16} />
              <span>Ver Dados Brutos da Tabela ({dados.length} registos)</span>
            </div>
            {showRawData ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>

          {showRawData && (
            <div className="accordion-content">
              <div className="table-responsive-wrapper">
                <table className="raw-data-table">
                  <thead>
                    <tr>
                      {tableColumns.map((col) => (
                        <th key={col}>{formatHeader(col)}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {dados.map((row, idx) => (
                      <tr key={idx}>
                        {tableColumns.map((col) => {
                          const val = row[col];
                          let displayVal = val;
                          if (typeof val === 'number') {
                            if (col.includes('congestionamento') || col.includes('pct') || col.includes('taxa')) {
                              displayVal = `${(val * 100).toFixed(1)}%`;
                            } else if (val % 1 !== 0) {
                              displayVal = val.toFixed(2);
                            } else {
                              displayVal = val.toLocaleString();
                            }
                          }
                          return <td key={col}>{displayVal !== null && displayVal !== undefined ? String(displayVal) : '-'}</td>;
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default RespostaCard;
