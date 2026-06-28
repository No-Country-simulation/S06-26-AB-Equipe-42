import React from 'react';

function IndicadorChart({ title, value, maxValue = 100, unit = '', color = 'var(--accent-cyan)' }) {
  const percentage = Math.min(100, Math.max(0, (value / maxValue) * 100));

  return (
    <div className="indicator-chart-wrapper">
      <div className="chart-info">
        <span className="chart-label">{title}</span>
        <span className="chart-value" style={{ color }}>
          {value.toLocaleString()} {unit}
        </span>
      </div>
      <div className="chart-track">
        <div 
          className="chart-fill" 
          style={{ 
            width: `${percentage}%`,
            background: color
          }}
        ></div>
      </div>
    </div>
  );
}

export default IndicadorChart;
