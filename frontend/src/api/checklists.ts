import apiClient from './client';

export interface Checklist {
  id: string;
  name: string;
  table_source: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ChecklistCreate {
  name: string;
}

export const checklistsApi = {
  getChecklists: async (includeVirtual: boolean = true): Promise<Checklist[]> => {
    const response = await apiClient.get<Checklist[]>('/api/checklists', {
      params: { include_virtual: includeVirtual }
    });
    return response.data;
  },

  getRealChecklists: async (): Promise<Checklist[]> => {
    const response = await apiClient.get<Checklist[]>('/api/checklists/real');
    return response.data;
  },

  createChecklist: async (data: ChecklistCreate): Promise<Checklist> => {
    const response = await apiClient.post<Checklist>('/api/checklists', data);
    return response.data;
  },

  deleteChecklist: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/checklists/${id}`);
  },

  bulkDeleteChecklists: async (ids: string[]): Promise<void> => {
    await apiClient.post('/api/checklists/bulk-delete', ids);
  },
};

