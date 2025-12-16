import apiClient from './client';
import { ImportResponse } from '../types';

export const importApi = {
  importExcel: async (file: File, tableSource?: string): Promise<ImportResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    if (tableSource) {
      formData.append('table_source', tableSource);
    }
    
    const response = await apiClient.post<ImportResponse>('/api/import/excel', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },
};

