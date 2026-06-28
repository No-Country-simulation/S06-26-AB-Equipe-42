import React, { useState } from 'react';
import { Search, Sparkles, CornerDownLeft } from 'lucide-react';

const SUGGESTIONS = [
  "Qual o cluster com maior congestionamento?",
  "Qual região tem a pior cobertura de sinal?",
  "Onde estão concentrados mais utilizadores?",
  "Como está o sinal em Cazenga?",
  "Quais clusters têm perfil corporativo?",
];

function AiQueryBar({ onSubmit, isLoading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;
    onSubmit(query);
  };

  const handleSuggestionClick = (suggestion) => {
    if (isLoading) return;
    setQuery(suggestion);
    onSubmit(suggestion);
  };

  return (
    <div className="query-bar-container">
      <form onSubmit={handleSubmit} className="query-form">
        <div className="query-input-wrapper">
          <Sparkles className="sparkles-icon" size={20} />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Pergunte ao AppBit... (Ex: Qual cluster tem mais tráfego?)"
            disabled={isLoading}
            className="query-input"
            required
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="query-submit-btn"
            aria-label="Submeter consulta"
          >
            {isLoading ? (
              <span className="spinner"></span>
            ) : (
              <>
                <span className="btn-text">Enviar</span>
                <CornerDownLeft size={16} className="enter-icon" />
              </>
            )}
          </button>
        </div>
      </form>

      <div className="suggestions-container">
        <span className="suggestions-title">Sugestões:</span>
        <div className="suggestions-list">
          {SUGGESTIONS.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              disabled={isLoading}
              className="suggestion-chip"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default AiQueryBar;
