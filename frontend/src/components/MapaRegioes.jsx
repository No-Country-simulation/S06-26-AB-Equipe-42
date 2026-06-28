import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';

const MAP_CENTER = [-27.55, -48.55];
const MAP_ZOOM = 11;

function MapaRegioes({ regions, selectedIndicator }) {
  const getMarkerRadius = (nUsuarios) => {
    return Math.sqrt(nUsuarios) * 0.25 + 6;
  };

  const getMarkerColor = (region) => {
    if (selectedIndicator === 'congestionamento_medio') {
      const value = region.congestionamento_medio;
      if (value < 0.3) return 'var(--color-success)';
      if (value < 0.6) return 'var(--color-warning)';
      return 'var(--color-danger)';
    }

    if (selectedIndicator === 'cobertura_sinal_dbm') {
      const value = region.cobertura_sinal_dbm;
      if (value >= -90) return 'var(--color-success)';
      if (value >= -105) return 'var(--color-warning)';
      return 'var(--color-danger)';
    }

    const value = region.n_usuarios;
    if (value < 200) return '#22d3ee';
    if (value < 800) return 'var(--accent-cyan)';
    return '#3b82f6';
  };

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <MapContainer 
        center={MAP_CENTER} 
        zoom={MAP_ZOOM} 
        scrollWheelZoom={true}
        style={{ width: '100%', height: '100%', minHeight: '450px' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {regions.map((region) => {
          const radius = getMarkerRadius(region.n_usuarios);
          const color = getMarkerColor(region);

          return (
            <CircleMarker
              key={region.id}
              center={[region.latitude, region.longitude]}
              radius={radius}
              pathOptions={{
                fillColor: color,
                color: '#ffffff',
                weight: 1,
                opacity: 0.5,
                fillOpacity: 0.7,
              }}
            >
              <Popup>
                <div className="map-popup-container">
                  <h4 className="popup-title">{region.nome_cluster}</h4>
                  <p className="popup-subtitle">{region.municipio} • Perfil: {region.perfil}</p>
                  
                  <table className="popup-table">
                    <tbody>
                      <tr>
                        <td><strong>Utilizadores Ativos:</strong></td>
                        <td>{region.n_usuarios.toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td><strong>Congestionamento Médio:</strong></td>
                        <td>
                          <span style={{ 
                            color: region.congestionamento_medio < 0.3 ? 'var(--color-success)' :
                                   region.congestionamento_medio < 0.6 ? 'var(--color-warning)' : 'var(--color-danger)',
                            fontWeight: '600'
                          }}>
                            {(region.congestionamento_medio * 100).toFixed(1)}%
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td><strong>Nível de Sinal (dBm):</strong></td>
                        <td>
                          <span style={{ 
                            color: region.cobertura_sinal_dbm >= -90 ? 'var(--color-success)' :
                                   region.cobertura_sinal_dbm >= -105 ? 'var(--color-warning)' : 'var(--color-danger)',
                            fontWeight: '600'
                          }}>
                            {region.cobertura_sinal_dbm} dBm
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
}

export default MapaRegioes;
