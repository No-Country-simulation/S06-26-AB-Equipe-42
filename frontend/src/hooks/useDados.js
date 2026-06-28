import { useQuery, useMutation } from '@tanstack/react-query';
import { apiService } from '../services/api.js';

export function useIntelligentQuery() {
  return useMutation({
    mutationFn: ({ consulta, filtros }) => {
      return apiService.postQuery(consulta, filtros);
    },
  });
}

export function useMapaData(indicador) {
  return useQuery({
    queryKey: ['mapaData', indicador],
    queryFn: () => apiService.getMapa(indicador),
    staleTime: 1000 * 60 * 5,
  });
}

export function useIndicadores() {
  return useQuery({
    queryKey: ['indicadores'],
    queryFn: apiService.getIndicadores,
    staleTime: 1000 * 60 * 60,
  });
}

export function useRegioes() {
  return useQuery({
    queryKey: ['regioes'],
    queryFn: apiService.getRegioes,
    staleTime: 1000 * 60 * 60,
  });
}
