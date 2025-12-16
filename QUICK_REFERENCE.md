# ⚡ Quick Reference — Шпаргалка разработчика

## 🚀 Быстрый старт

```bash
# 1. Клон + вход
git clone <repo>
cd compliance-monitor

# 2. Docker Compose
docker-compose up -d

# 3. Миграции БД
docker exec compliance-monitor-backend alembic upgrade head

# 4. Открыть в браузере
Frontend:  http://localhost:3000
Backend:   http://localhost:8000
Swagger:   http://localhost:8000/docs
```

---

## 📊 Структура проекта

```
project/
├── backend/                    # Python/FastAPI
│   ├── app/
│   │   ├── main.py            # Entry point FastAPI
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/               # Endpoints
│   │   └── services/          # Business logic
│   ├── migrations/            # Alembic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React/TypeScript
│   ├── src/
│   │   ├── components/        # React компоненты
│   │   ├── api/               # API client
│   │   ├── types/             # TS types
│   │   └── main.tsx
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

---

## 🗄️ Database Schema

### Таблица: `process_records`

```sql
id (UUID) PRIMARY KEY
process_name (VARCHAR 255) NOT NULL
product_type (VARCHAR 100)
status (VARCHAR 50) NOT NULL
date_kb (DATE)
fio_customer (VARCHAR 255)
date_bank_receipt (DATE)
fio_bank_officer (VARCHAR 255)
process_number (INT)
bank_employee_name (VARCHAR 255)
comments (TEXT)
table_source (VARCHAR 100) NOT NULL
import_batch_id (VARCHAR 100)
import_date (TIMESTAMP)
is_archived (BOOLEAN)
created_at (TIMESTAMP)
updated_at (TIMESTAMP)
```

**Constraints:**
```sql
CHECK (status IN ('Выполнено', 'Успешно', 'В работе', 'Не начато', 'Не успешно'))
CHECK (table_source IN ('safes_rental', 'deposits_fl', 'deposits_ul', 'credits_fl', 'payment_orders', 'payment_processing'))
```

**Индексы:**
```sql
CREATE INDEX idx_status ON process_records(status);
CREATE INDEX idx_table_source ON process_records(table_source);
CREATE INDEX idx_import_batch ON process_records(import_batch_id);
CREATE INDEX idx_process_name ON process_records(process_name);
```

---

## 🔌 API Endpoints Cheat Sheet

| Метод | Path | Быстрая помощь |
|-------|------|----------------|
| GET | `/api/dashboard/summary` | % прогресса, сводка по статусам |
| GET | `/api/records?table_source=safes_rental&status=Выполнено` | Получить записи (фильтр, сортировка) |
| POST | `/api/records` | Создать запись (JSON body) |
| PUT | `/api/records/{id}` | Обновить запись |
| DELETE | `/api/records/{id}` | Удалить запись |
| POST | `/api/records/bulk-delete` | Удалить несколько `{"ids": []}` |
| POST | `/api/import/excel` | Upload файл (multipart/form-data) |
| GET | `/api/import/logs` | История импортов |
| GET | `/api/export/excel` | Скачать Excel со всеми данными |

---

## 🐍 Backend Python Snippets

### Модель

```python
from sqlalchemy import Column, String, Date, Text, Boolean, DateTime
from datetime import datetime
import uuid

class ProcessRecord(Base):
    __tablename__ = "process_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    process_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    table_source = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Pydantic Schema

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ProcessRecordCreate(BaseModel):
    process_name: str
    product_type: Optional[str] = None
    status: str  # enum check
    table_source: str
    date_kb: Optional[date] = None
    comments: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "process_name": "Добавление договора",
                "product_type": "Аренда Сейфов",
                "status": "Выполнено",
                "table_source": "safes_rental"
            }
        }
```

### CRUD Endpoint

```python
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/records")

@router.get("")
def get_records(
    db: Session = Depends(get_db),
    table_source: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(ProcessRecord)
    if table_source:
        query = query.filter_by(table_source=table_source)
    if status:
        query = query.filter_by(status=status)
    return query.offset(skip).limit(limit).all()

@router.post("", status_code=201)
def create_record(record: ProcessRecordCreate, db: Session = Depends(get_db)):
    db_record = ProcessRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.put("/{record_id}")
def update_record(record_id: str, record: ProcessRecordCreate, db: Session = Depends(get_db)):
    db_record = db.query(ProcessRecord).filter_by(id=record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    for key, value in record.dict().items():
        setattr(db_record, key, value)
    db.commit()
    return db_record

@router.delete("/{record_id}")
def delete_record(record_id: str, db: Session = Depends(get_db)):
    db_record = db.query(ProcessRecord).filter_by(id=record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(db_record)
    db.commit()
    return {"deleted": True}
```

### Excel Import

```python
import openpyxl
from typing import List, Tuple

def parse_excel_file(file_path: str, table_source: str) -> Tuple[List[dict], List[str]]:
    """Парсит Excel и маппит на структуру БД"""
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    
    headers = [cell.value for cell in ws[1]]
    records = []
    errors = []
    
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        row_data = {h: row[i] for i, h in enumerate(headers)}
        
        # Маппинг
        mapped = map_excel_to_record(row_data, table_source)
        
        # Валидация
        if not is_valid(mapped):
            errors.append(f"Row {row_idx}: Invalid data")
            continue
        
        records.append(mapped)
    
    return records, errors

@router.post("/import/excel")
async def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    records, errors = parse_excel_file(file.file, detected_source)
    
    for record in records:
        db.add(ProcessRecord(**record))
    db.commit()
    
    return {
        "success_rows": len(records),
        "error_rows": len(errors),
        "errors": errors[:10]
    }
```

---

## ⚛️ Frontend React Snippets

### Компонент таблицы

```tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const TableView: React.FC<{ tableSource: string }> = ({ tableSource }) => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');

  useEffect(() => {
    fetchRecords();
  }, [tableSource]);

  const fetchRecords = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/records', {
        params: { table_source: tableSource }
      });
      setRecords(res.data);
    } finally {
      setLoading(false);
    }
  };

  const handleCellEdit = async (id: string, field: string, value: string) => {
    try {
      await axios.put(`/api/records/${id}`, { [field]: value });
      fetchRecords();
    } catch (err) {
      console.error('Update failed', err);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Delete record?')) {
      try {
        await axios.delete(`/api/records/${id}`);
        fetchRecords();
      } catch (err) {
        console.error('Delete failed', err);
      }
    }
  };

  return (
    <div>
      <table border={1}>
        <thead>
          <tr>
            <th>Process Name</th>
            <th>Status</th>
            <th>Date KB</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {records.map((record: any) => (
            <tr key={record.id}>
              <td 
                onDoubleClick={() => {
                  setEditingId(record.id);
                  setEditValue(record.process_name);
                }}
              >
                {editingId === record.id ? (
                  <input 
                    value={editValue} 
                    onChange={(e) => setEditValue(e.target.value)}
                    onBlur={() => {
                      handleCellEdit(record.id, 'process_name', editValue);
                      setEditingId(null);
                    }}
                  />
                ) : (
                  record.process_name
                )}
              </td>
              <td>{record.status}</td>
              <td>{record.date_kb}</td>
              <td>
                <button onClick={() => handleDelete(record.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### Dashboard компонент

```tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [records, setRecords] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    const res = await axios.get('/api/dashboard/summary');
    setSummary(res.data);
    
    const recs = await axios.get('/api/records');
    setRecords(recs.data);
  };

  const renderProgressGrid = () => {
    const statusColorMap: Record<string, string> = {
      'Выполнено': '#4ade80', // green
      'Успешно': '#4ade80',
      'В работе': '#facc15', // yellow
      'Не начато': '#d1d5db', // gray
      'Не успешно': '#ef4444', // red
    };

    return (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(10, 1fr)', gap: '4px' }}>
        {records.map((record) => (
          <div
            key={record.id}
            style={{
              width: '20px',
              height: '20px',
              backgroundColor: statusColorMap[record.status] || '#d1d5db',
              borderRadius: '2px',
              cursor: 'pointer',
              title: `${record.process_name} - ${record.status}`
            }}
            title={record.process_name}
          />
        ))}
      </div>
    );
  };

  if (!summary) return <div>Loading...</div>;

  return (
    <div>
      <h1>Compliance Progress Monitor</h1>
      
      <div style={{ fontSize: '2em', fontWeight: 'bold' }}>
        {summary.progress_percent}% ({summary.completed}/{summary.total_records})
      </div>
      
      <p>Completed: {summary.completed}</p>
      <p>In Progress: {summary.in_progress}</p>
      <p>Not Started: {summary.not_started}</p>
      
      <h3>Progress Grid</h3>
      {renderProgressGrid()}
    </div>
  );
};
```

### Import Dialog

```tsx
import React, { useState } from 'react';
import axios from 'axios';

export const ImportDialog: React.FC<{ onSuccess: () => void }> = ({ onSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleImport = async () => {
    if (!file) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const res = await axios.post('/api/import/excel', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data);
      onSuccess();
    } catch (err) {
      console.error('Import failed', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        type="file" 
        accept=".xlsx" 
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleImport} disabled={!file || loading}>
        {loading ? 'Importing...' : 'Import'}
      </button>
      
      {result && (
        <div>
          <p>Success: {result.success_rows}</p>
          <p>Errors: {result.error_rows}</p>
          {result.errors && (
            <ul>
              {result.errors.map((err: any, idx: number) => (
                <li key={idx}>Row {err.row}, {err.field}: {err.message}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};
```

---

## 🧪 Testing

### pytest fixtures

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db():
    """In-memory SQLite for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

@pytest.fixture
def client(db):
    """FastAPI TestClient"""
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app)
```

### Unit test example

```python
def test_create_record(client):
    response = client.post("/api/records", json={
        "process_name": "Test",
        "status": "Выполнено",
        "table_source": "safes_rental"
    })
    assert response.status_code == 201
    assert response.json()["process_name"] == "Test"

def test_get_records(client, db):
    # Setup
    record = ProcessRecord(
        process_name="Test",
        status="Выполнено",
        table_source="safes_rental"
    )
    db.add(record)
    db.commit()
    
    # Test
    response = client.get("/api/records")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_dashboard_summary(client, db):
    # Setup: создаём несколько записей
    for i in range(10):
        db.add(ProcessRecord(
            process_name=f"Test {i}",
            status="Выполнено" if i < 7 else "В работе",
            table_source="safes_rental"
        ))
    db.commit()
    
    # Test
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] == 10
    assert data["completed"] == 7
    assert data["progress_percent"] == 70
```

---

## 🐳 Docker Commands

```bash
# Запуск всего
docker-compose up -d

# Логи
docker-compose logs -f backend
docker-compose logs -f frontend

# Заход в контейнер
docker exec -it compliance-monitor-backend bash

# Остановка
docker-compose down

# Переоздание (если изменились Dockerfile)
docker-compose up -d --build

# Очистка данных (удалить volume)
docker-compose down -v
```

---

## 🔄 Migration Commands

```bash
# Инициализация (первый раз)
cd backend
alembic init -t async migrations

# Создание миграции
alembic revision --autogenerate -m "Add status column"

# Просмотр версий
alembic current
alembic history

# Применение
alembic upgrade head

# Откат на одну версию назад
alembic downgrade -1

# Откат полностью
alembic downgrade base
```

---

## 📝 Environment Variables

```bash
# backend/.env
ENVIRONMENT=development
DATABASE_URL=postgresql://compliance:password@postgres:5432/compliance_db
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:3000"]

# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🔍 Debugging

### Backend logging

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Processing record: {record_id}")
logger.warning(f"Validation warning: {field}")
logger.error(f"Import failed: {error}", exc_info=True)
```

### Frontend debugging (React DevTools)

```javascript
// Console
console.log('Records:', records);
console.error('API Error:', error);
console.time('operation');
// ... code ...
console.timeEnd('operation');
```

---

## 📚 Полезные ссылки

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLAlchemy ORM: https://docs.sqlalchemy.org/
- React Docs: https://react.dev/
- PostgreSQL: https://www.postgresql.org/docs/
- Docker: https://docs.docker.com/
- Pydantic: https://docs.pydantic.dev/

---

## ✅ Чек-лист перед деплоем

- [ ] Все тесты проходят (`pytest`)
- [ ] Линтер чистый (`flake8`, `eslint`)
- [ ] БД миграции применены (`alembic upgrade head`)
- [ ] Environment variables установлены
- [ ] Docker images собраны
- [ ] API docs доступны (`/docs`)
- [ ] Frontend и backend связаны
- [ ] Логирование работает
- [ ] Ошибки обрабатываются gracefully
- [ ] README и docs актуальны

---

**Дата:** 12 декабря 2025  
**Версия:** 1.0  
**Для вопросов:** см. полное ТЗ в `TZ_CFT_Compliance_Monitor.md`
