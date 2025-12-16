import { useState } from 'react';
import { checklistsApi } from '../api/checklists';
import './AddChecklistModal.css';

interface AddChecklistModalProps {
  onClose: () => void;
  onSuccess: () => void;
}

const AddChecklistModal = ({ onClose, onSuccess }: AddChecklistModalProps) => {
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!name.trim()) {
      setError('Введите название чек-листа');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await checklistsApi.createChecklist({ name: name.trim() });
      onSuccess();
    } catch (err: any) {
      // Обрабатываем ошибки API
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('Ошибка создания чек-листа');
      }
      console.error('Create checklist error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Добавить чек-лист</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && (
              <div className="error-message">{error}</div>
            )}

            <div className="form-group">
              <label>
                Название чек-листа <span className="required">*</span>
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => {
                  setName(e.target.value);
                  setError(null);
                }}
                placeholder="Введите название чек-листа"
                required
                autoFocus
                disabled={loading}
              />
            </div>
          </div>

          <div className="modal-footer">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
              disabled={loading}
            >
              Отмена
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Создание...' : 'Создать'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddChecklistModal;

