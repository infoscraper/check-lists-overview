import apiClient from './client';

export const exportApi = {
  exportExcel: async (table_source?: string): Promise<Blob> => {
    const response = await apiClient.get('/api/export/excel', {
      params: { table_source },
      responseType: 'blob',
    });
    
    return response.data;
  },
};

