import { useState, useEffect, useCallback } from 'react';
import { recordsApi } from '../api/records';
import { exportApi } from '../api/export';
import { checklistsApi, Checklist } from '../api/checklists';
import { ProcessRecord } from '../types';
import ImportDialog from './ImportDialog';
import RecordModal from './RecordModal';
import AddChecklistModal from './AddChecklistModal';
import DeleteChecklistModal from './DeleteChecklistModal';
import { EditIcon, DeleteIcon, UploadIcon, DownloadIcon, AddIcon } from './Icons';
import './TableView.css';

const TableView = () => {
  const [checklists, setChecklists] = useState<Checklist[]>([]);
  const [activeTab, setActiveTab] = useState<string>('');
  const [records, setRecords] = useState<ProcessRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showImportDialog, setShowImportDialog] = useState(false);
  const [showRecordModal, setShowRecordModal] = useState(false);
  const [showAddChecklistModal, setShowAddChecklistModal] = useState(false);
  const [showDeleteChecklistModal, setShowDeleteChecklistModal] = useState(false);
  const [editingRecord, setEditingRecord] = useState<ProcessRecord | null>(null);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());


  const fetchChecklists = useCallback(async () => {
    try {
      const checklistsData = await checklistsApi.getChecklists();
      
      // Если получили данные, используем их
      if (checklistsData && checklistsData.length > 0) {
        setChecklists(checklistsData);
        
        // Если активный таб не найден в списке, устанавливаем первый доступный
        const found = checklistsData.find(c => c.table_source === activeTab);
        if (!found && checklistsData.length > 0) {
          setActiveTab(checklistsData[0].table_source);
        }
      } else {
        // Если список пустой, очищаем
        setChecklists([]);
        setActiveTab('');
      }
    } catch (err) {
      console.error('Fetch checklists error:', err);
      // При ошибке очищаем
      setChecklists([]);
      setActiveTab('');
    }
  }, [activeTab]);

  const fetchRecords = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await recordsApi.getRecords({
        table_source: activeTab,
        limit: 1000,
      });
      setRecords(response.records);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка загрузки данных');
      console.error('Fetch records error:', err);
    } finally {
      setLoading(false);
    }
  }, [activeTab]);

  useEffect(() => {
    // Загружаем чек-листы из API
    fetchChecklists();
  }, []);

  useEffect(() => {
    if (activeTab && activeTab.trim() !== '') {
      fetchRecords();
    }
  }, [activeTab, fetchRecords]);

  const handleImport = async () => {
    setShowImportDialog(true);
  };

  const handleImportSuccess = () => {
    setShowImportDialog(false);
    fetchRecords();
  };

  const handleAddChecklistSuccess = async () => {
    setShowAddChecklistModal(false);
    // Обновляем список чек-листов
    const updatedChecklists = await checklistsApi.getChecklists();
    setChecklists(updatedChecklists);
    
    // Устанавливаем последний созданный чек-лист как активный
    if (updatedChecklists.length > 0) {
      const lastChecklist = updatedChecklists[updatedChecklists.length - 1];
      setActiveTab(lastChecklist.table_source);
    }
  };

  const handleDeleteChecklistSuccess = async () => {
    setShowDeleteChecklistModal(false);
    // Обновляем список чек-листов
    const updatedChecklists = await checklistsApi.getChecklists();
    setChecklists(updatedChecklists);
    
    // Если удаленный чек-лист был активным, переключаемся на первый доступный
    if (updatedChecklists.length > 0) {
      const found = updatedChecklists.find(c => c.table_source === activeTab);
      if (!found) {
        setActiveTab(updatedChecklists[0].table_source);
      }
    } else {
      // Если все удалены, очищаем
      setChecklists([]);
      setActiveTab('');
    }
  };

  const handleExport = async () => {
    try {
      const blob = await exportApi.exportExcel(activeTab);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `process_records_${activeTab}.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Export error:', err);
      alert('Ошибка экспорта');
    }
  };

  const handleAdd = () => {
    setEditingRecord(null);
    setShowRecordModal(true);
  };

  const handleEdit = (record: ProcessRecord) => {
    setEditingRecord(record);
    setShowRecordModal(true);
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Удалить запись?')) return;
    
    try {
      await recordsApi.deleteRecord(id);
      fetchRecords();
    } catch (err) {
      console.error('Delete error:', err);
      alert('Ошибка удаления');
    }
  };

  const handleBulkDelete = async () => {
    if (selectedIds.size === 0) return;
    if (!window.confirm(`Удалить ${selectedIds.size} записей?`)) return;

    try {
      await recordsApi.bulkDelete(Array.from(selectedIds));
      setSelectedIds(new Set());
      fetchRecords();
    } catch (err) {
      console.error('Bulk delete error:', err);
      alert('Ошибка удаления');
    }
  };

  const toggleSelect = (id: string) => {
    const newSelected = new Set(selectedIds);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedIds(newSelected);
  };

  const toggleSelectAll = () => {
    if (selectedIds.size === records.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(records.map(r => r.id)));
    }
  };

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return '--';
    try {
      return new Date(dateStr).toLocaleDateString('ru-RU');
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="table-view">
      <div className="table-header">
        <h2>Детализация чек-листов</h2>
        <div className="table-actions">
          <button onClick={handleImport} className="btn btn-primary">
            <UploadIcon />
            Импортировать Excel
          </button>
          <button onClick={handleExport} className="btn btn-secondary">
            <DownloadIcon />
            Экспортировать
          </button>
          {selectedIds.size > 0 && (
            <button onClick={handleBulkDelete} className="btn btn-danger">
              <DeleteIcon />
              Удалить выбранные ({selectedIds.size})
            </button>
          )}
        </div>
      </div>

      <div className="tabs-container">
        <div className="tabs">
          {checklists.map((checklist) => (
            <button
              key={checklist.id}
              className={`tab ${activeTab === checklist.table_source ? 'active' : ''}`}
              onClick={() => setActiveTab(checklist.table_source)}
            >
              {checklist.name}
            </button>
          ))}
        </div>
      </div>

      <div className="checklist-actions-container">
        <button 
          onClick={handleAdd} 
          className="btn btn-primary btn-checklist-action btn-add-record"
        >
          <AddIcon />
          Добавить запись
        </button>
        <button 
          onClick={() => setShowAddChecklistModal(true)} 
          className="btn btn-success btn-checklist-action"
        >
          <AddIcon />
          Добавить чек-лист
        </button>
        <button 
          onClick={() => setShowDeleteChecklistModal(true)} 
          className="btn btn-danger btn-checklist-action"
        >
          <DeleteIcon />
          Удалить чек-лист
        </button>
      </div>

      {loading && <div className="loading">Загрузка...</div>}
      {error && <div className="error">Ошибка: {error}</div>}

      {!loading && !error && (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>
                  <input
                    type="checkbox"
                    checked={selectedIds.size === records.length && records.length > 0}
                    onChange={toggleSelectAll}
                  />
                </th>
                <th>Наименование процесса</th>
                <th>Продукт</th>
                <th>Статус</th>
                <th>Дата КБ</th>
                <th>ФИО клиента</th>
                <th>Дата приемки</th>
                <th>ФИО от Банка</th>
                <th>Комментарий</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {records.length === 0 ? (
                <tr>
                  <td colSpan={10} className="empty-state">
                    Нет данных
                  </td>
                </tr>
              ) : (
                records.map((record) => (
                  <tr key={record.id}>
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedIds.has(record.id)}
                        onChange={() => toggleSelect(record.id)}
                      />
                    </td>
                    <td>{record.process_name}</td>
                    <td>{record.product_type || '--'}</td>
                    <td>
                      <span className={`status-badge status-${record.status.toLowerCase().replace(' ', '-')}`}>
                        {record.status}
                      </span>
                    </td>
                    <td>{formatDate(record.date_kb)}</td>
                    <td>{record.fio_customer || '--'}</td>
                    <td>{formatDate(record.date_bank_receipt)}</td>
                    <td>{record.fio_bank_officer || '--'}</td>
                    <td className="comments-cell">{record.comments || '--'}</td>
                    <td>
                      <div className="action-buttons">
                        <button
                          onClick={() => handleEdit(record)}
                          className="btn-icon btn-edit"
                          title="Редактировать"
                        >
                          <EditIcon />
                        </button>
                        <button
                          onClick={() => handleDelete(record.id)}
                          className="btn-icon btn-delete"
                          title="Удалить"
                        >
                          <DeleteIcon />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {showImportDialog && (
        <ImportDialog
          tableSource={activeTab}
          onClose={() => setShowImportDialog(false)}
          onSuccess={handleImportSuccess}
        />
      )}

      {showRecordModal && (
        <RecordModal
          record={editingRecord}
          tableSource={activeTab}
          onClose={() => {
            setShowRecordModal(false);
            setEditingRecord(null);
          }}
          onSuccess={() => {
            setShowRecordModal(false);
            setEditingRecord(null);
            fetchRecords();
          }}
        />
      )}

      {showAddChecklistModal && (
        <AddChecklistModal
          onClose={() => setShowAddChecklistModal(false)}
          onSuccess={handleAddChecklistSuccess}
        />
      )}

      {showDeleteChecklistModal && (
        <DeleteChecklistModal
          onClose={() => setShowDeleteChecklistModal(false)}
          onSuccess={handleDeleteChecklistSuccess}
        />
      )}
    </div>
  );
};

export default TableView;

