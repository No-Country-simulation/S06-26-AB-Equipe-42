import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  postQuery: async (consulta, filtros = {}) => {
    const response = await apiClient.post('/dados', {
      consulta,
      filtros,
      idioma: 'pt',
    });
    return response.data;
  },

  getMapa: async (indicador) => {
    const params = {};
    if (indicador) {
      params.indicador = indicador;
    }
    const response = await apiClient.get('/mapa', { params });
    return response.data;
  },

  getIndicadores: async () => {
    const response = await apiClient.get('/indicadores');
    return response.data;
  },

  getRegioes: async () => {
    const response = await apiClient.get('/regioes');
    return response.data;
  },
};

export default apiClient;
