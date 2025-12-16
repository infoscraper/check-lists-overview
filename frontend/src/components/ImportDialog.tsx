import { useState } from 'react';
import { importApi } from '../api/import';
import { ImportResponse } from '../types';
import './ImportDialog.css';

interface ImportDialogProps {
  tableSource?: string;
  onClose: () => void;
  onSuccess: () => void;
}

const ImportDialog = ({ tableSource, onClose, onSuccess }: ImportDialogProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ImportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleImport = async () => {
    if (!file || loading) return; // Предотвращаем повторный вызов

    try {
      setLoading(true);
      setError(null);
      const response = await importApi.importExcel(file, tableSource);
      setResult(response);
      
      if (response.error_rows === 0) {
        setTimeout(() => {
          onSuccess();
        }, 2000);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка импорта');
      console.error('Import error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Импорт данных из Excel</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="file-input-container">
            <label className="file-input-label">
              <input
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileChange}
                disabled={loading}
                className="file-input"
              />
              <span className="file-input-text">
                {file ? file.name : 'Выберите файл Excel'}
              </span>
            </label>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {result && (
            <div className="import-result">
              <h4>Результаты импорта:</h4>
              <div className="result-stats">
                <div className="stat-item">
                  <span className="stat-label">Всего строк:</span>
                  <span className="stat-value">{result.total_rows}</span>
                </div>
                <div className="stat-item success">
                  <span className="stat-label">Успешно:</span>
                  <span className="stat-value">{result.success_rows}</span>
                </div>
                <div className="stat-item error">
                  <span className="stat-label">Ошибок:</span>
                  <span className="stat-value">{result.error_rows}</span>
                </div>
              </div>

              {result.errors && result.errors.length > 0 && (
                <div className="errors-list">
                  <h5>Ошибки валидации:</h5>
                  <div className="errors-scroll">
                    {result.errors.map((err, idx) => (
                      <div key={idx} className="error-item">
                        <strong>Строка {err.row}</strong> ({err.field}): {err.message}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button
            onClick={handleImport}
            disabled={!file || loading}
            className="btn btn-primary"
          >
            {loading ? 'Импорт...' : 'Импортировать'}
          </button>
          <button onClick={onClose} className="btn btn-secondary">
            Закрыть
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImportDialog;

