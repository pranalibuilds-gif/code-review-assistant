import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

export const useSystemHealth = () => {
  return useQuery({
    queryKey: ['system', 'health'],
    queryFn: async () => {
      const response = await client.get('/health');
      return response.data;
    },
    refetchInterval: 30000, // Poll every 30 seconds
  });
};
