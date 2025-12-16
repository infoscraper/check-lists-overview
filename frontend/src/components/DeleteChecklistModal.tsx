import { useState, useEffect } from 'react';
import { checklistsApi, Checklist } from '../api/checklists';
import './DeleteChecklistModal.css';

interface DeleteChecklistModalProps {
  onClose: () => void;
  onSuccess: () => void;
}

const DeleteChecklistModal = ({ onClose, onSuccess }: DeleteChecklistModalProps) => {
  const [checklists, setChecklists] = useState<Checklist[]>([]);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Стандартные чек-листы, которые нельзя удалить
  const standardSources = [
    'safes_rental',
    'deposits_fl',
    'deposits_ul',
    'credits_fl',
    'payment_orders',
    'payment_processing',
  ];

  useEffect(() => {
    const fetchChecklists = async () => {
      try {
        setLoading(true);
        // Получаем только реальные чек-листы (созданные пользователем), без виртуальных
        const data = await checklistsApi.getRealChecklists();
        console.log('Real checklists from API:', data);
        
        // Фильтруем только те, которые можно удалить (не стандартные)
        const deletable = data.filter(c => {
          // Исключаем стандартные источники
          return !standardSources.includes(c.table_source);
        });
        
        console.log('Deletable checklists:', deletable);
        setChecklists(deletable);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Ошибка загрузки чек-листов');
        console.error('Fetch checklists error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchChecklists();
  }, []);

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
    if (selectedIds.size === checklists.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(checklists.map(c => c.id)));
    }
  };

  const handleDelete = async () => {
    if (selectedIds.size === 0) {
      setError('Выберите хотя бы один чек-лист для удаления');
      return;
    }

    if (!window.confirm(`Удалить ${selectedIds.size} чек-лист(ов)?`)) {
      return;
    }

    try {
      setDeleting(true);
      setError(null);
      await checklistsApi.bulkDeleteChecklists(Array.from(selectedIds));
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка удаления чек-листов');
      console.error('Delete checklists error:', err);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Удалить чек-лист</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {error && (
            <div className="error-message">{error}</div>
          )}

          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : checklists.length === 0 ? (
            <div className="empty-message">
              Нет чек-листов для удаления. Стандартные чек-листы нельзя удалить.
            </div>
          ) : (
            <>
              <div className="delete-checklist-header">
                <label className="select-all-checkbox">
                  <input
                    type="checkbox"
                    checked={selectedIds.size === checklists.length && checklists.length > 0}
                    onChange={toggleSelectAll}
                  />
                  <span>Выбрать все ({checklists.length})</span>
                </label>
                {selectedIds.size > 0 && (
                  <span className="selected-count">
                    Выбрано: {selectedIds.size}
                  </span>
                )}
              </div>

              <div className="checklists-list">
                {checklists.map((checklist) => (
                  <label key={checklist.id} className="checklist-item">
                    <input
                      type="checkbox"
                      checked={selectedIds.has(checklist.id)}
                      onChange={() => toggleSelect(checklist.id)}
                    />
                    <span className="checklist-name">{checklist.name}</span>
                    <span className="checklist-source">({checklist.table_source})</span>
                  </label>
                ))}
              </div>
            </>
          )}
        </div>

        <div className="modal-footer">
          <button
            type="button"
            onClick={onClose}
            className="btn btn-secondary"
            disabled={deleting}
          >
            Отмена
          </button>
          {checklists.length > 0 && (
            <button
              type="button"
              onClick={handleDelete}
              className="btn btn-danger"
              disabled={deleting || selectedIds.size === 0}
            >
              {deleting ? 'Удаление...' : `Удалить (${selectedIds.size})`}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default DeleteChecklistModal;

