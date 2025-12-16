import apiClient from './client';
import { ProcessRecord, ProcessRecordCreate, ProcessRecordUpdate } from '../types';

export interface GetRecordsParams {
  table_source?: string;
  status?: string;
  search?: string;
  skip?: number;
  limit?: number;
}

export interface RecordsResponse {
  records: ProcessRecord[];
  total: number;
  skip: number;
  limit: number;
}

export const recordsApi = {
  getRecords: async (params?: GetRecordsParams): Promise<RecordsResponse> => {
    const response = await apiClient.get<RecordsResponse>('/api/records', { params });
    return response.data;
  },

  getRecord: async (id: string): Promise<ProcessRecord> => {
    const response = await apiClient.get<ProcessRecord>(`/api/records/${id}`);
    return response.data;
  },

  createRecord: async (record: ProcessRecordCreate): Promise<ProcessRecord> => {
    const response = await apiClient.post<ProcessRecord>('/api/records', record);
    return response.data;
  },

  updateRecord: async (id: string, record: ProcessRecordUpdate): Promise<ProcessRecord> => {
    const response = await apiClient.put<ProcessRecord>(`/api/records/${id}`, record);
    return response.data;
  },

  deleteRecord: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/records/${id}`);
  },

  bulkDelete: async (ids: string[]): Promise<{ deleted: number }> => {
    const response = await apiClient.post<{ deleted: number }>('/api/records/bulk-delete', ids);
    return response.data;
  },
};

