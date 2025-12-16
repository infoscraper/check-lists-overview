import { useState, useEffect } from 'react';
import { recordsApi } from '../api/records';
import { ProcessRecord, ProcessRecordCreate, ProcessRecordUpdate } from '../types';
import './RecordModal.css';

interface RecordModalProps {
  record: ProcessRecord | null;
  tableSource: string;
  onClose: () => void;
  onSuccess: () => void;
}

const STATUS_OPTIONS = ['Выполнено', 'Успешно', 'В работе', 'Не начато', 'Не успешно'];

const RecordModal = ({ record, tableSource, onClose, onSuccess }: RecordModalProps) => {
  const [formData, setFormData] = useState<ProcessRecordCreate | ProcessRecordUpdate>({
    process_name: '',
    product_type: '',
    status: 'Не начато',
    table_source: tableSource,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (record) {
      setFormData({
        process_name: record.process_name,
        product_type: record.product_type || '',
        status: record.status,
        date_kb: record.date_kb || undefined,
        fio_customer: record.fio_customer || '',
        date_bank_receipt: record.date_bank_receipt || undefined,
        fio_bank_officer: record.fio_bank_officer || '',
        process_number: record.process_number || undefined,
        bank_employee_name: record.bank_employee_name || '',
        comments: record.comments || '',
      });
    }
  }, [record]);

  const handleChange = (field: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.process_name?.trim()) {
      setError('Укажите название процесса');
      return;
    }

    if (!formData.status) {
      setError('Выберите статус');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      if (record) {
        // Обновление
        await recordsApi.updateRecord(record.id, formData as ProcessRecordUpdate);
      } else {
        // Создание
        await recordsApi.createRecord(formData as ProcessRecordCreate);
      }

      onSuccess();
    } catch (err: any) {
      console.error('Save error:', err);
      let errorMessage = 'Ошибка сохранения';
      
      if (err?.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err?.message) {
        errorMessage = err.message;
      } else if (err?.response?.status === 500) {
        errorMessage = 'Ошибка сервера. Проверьте логи бэкенда.';
      } else if (err?.response?.status === 400) {
        errorMessage = 'Неверные данные. Проверьте заполнение полей.';
      } else if (err?.code === 'ECONNREFUSED' || err?.message?.includes('Network Error')) {
        errorMessage = 'Ошибка подключения к серверу. Проверьте, что бэкенд запущен.';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{record ? 'Редактировать запись' : 'Добавить запись'}</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="record-form">
          <div className="modal-body">
            {error && (
              <div className="error-message">{error}</div>
            )}

            <div className="form-grid">
              <div className="form-group form-group-full">
                <label>
                  Наименование процесса <span className="required">*</span>
                </label>
                <input
                  type="text"
                  value={formData.process_name || ''}
                  onChange={(e) => handleChange('process_name', e.target.value)}
                  placeholder="Введите название процесса"
                  required
                  autoFocus
                />
              </div>

              <div className="form-group">
                <label>
                  Статус <span className="required">*</span>
                </label>
                <select
                  value={formData.status || 'Не начато'}
                  onChange={(e) => handleChange('status', e.target.value)}
                  required
                >
                  {STATUS_OPTIONS.map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
              </div>

              {record && (
                <>
                  <div className="form-group">
                    <label>Продукт</label>
                    <input
                      type="text"
                      value={formData.product_type || ''}
                      onChange={(e) => handleChange('product_type', e.target.value)}
                    />
                  </div>

                  <div className="form-group">
                    <label>Дата КБ</label>
                    <input
                      type="date"
                      value={formData.date_kb || ''}
                      onChange={(e) => handleChange('date_kb', e.target.value || undefined)}
                    />
                  </div>

                  <div className="form-group">
                    <label>ФИО клиента</label>
                    <input
                      type="text"
                      value={formData.fio_customer || ''}
                      onChange={(e) => handleChange('fio_customer', e.target.value || undefined)}
                    />
                  </div>

                  <div className="form-group">
                    <label>Дата приемки Банк</label>
                    <input
                      type="date"
                      value={formData.date_bank_receipt || ''}
                      onChange={(e) => handleChange('date_bank_receipt', e.target.value || undefined)}
                    />
                  </div>

                  <div className="form-group">
                    <label>ФИО от Банка</label>
                    <input
                      type="text"
                      value={formData.fio_bank_officer || ''}
                      onChange={(e) => handleChange('fio_bank_officer', e.target.value || undefined)}
                    />
                  </div>

                  <div className="form-group">
                    <label>НПП</label>
                    <input
                      type="number"
                      value={formData.process_number || ''}
                      onChange={(e) => handleChange('process_number', e.target.value ? parseInt(e.target.value) : undefined)}
                    />
                  </div>

                  <div className="form-group">
                    <label>Сотрудник банка</label>
                    <input
                      type="text"
                      value={formData.bank_employee_name || ''}
                      onChange={(e) => handleChange('bank_employee_name', e.target.value || undefined)}
                    />
                  </div>

                  <div className="form-group form-group-full">
                    <label>Комментарий</label>
                    <textarea
                      value={formData.comments || ''}
                      onChange={(e) => handleChange('comments', e.target.value || undefined)}
                      rows={3}
                    />
                  </div>
                </>
              )}
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
              {loading ? 'Сохранение...' : 'Сохранить'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RecordModal;

