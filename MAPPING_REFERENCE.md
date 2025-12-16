# 📋 Справочник маппинга колонок Excel → БД

## Унифицированная схема таблицы `process_records`

```python
# models/process_record.py
from sqlalchemy import Column, String, Date, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class ProcessRecord(Base):
    __tablename__ = "process_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Основные данные
    process_name = Column(String(255), nullable=False)
    product_type = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False)  # enum: Выполнено, Успешно, В работе, Не начато, Не успешно
    
    # Даты и лица
    date_kb = Column(Date, nullable=True)
    fio_customer = Column(String(255), nullable=True)
    date_bank_receipt = Column(Date, nullable=True)
    fio_bank_officer = Column(String(255), nullable=True)
    
    # Доп. поля
    process_number = Column(Integer, nullable=True)
    bank_employee_name = Column(String(255), nullable=True)
    comments = Column(Text, nullable=True)
    
    # Служебные поля
    table_source = Column(String(100), nullable=False)  # enum
    import_batch_id = Column(String(100), nullable=True)
    import_date = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

## Маппинг по таблицам (источникам)

### 1️⃣ АРЕНДА СЕЙФОВ (safes_rental)

**Исходные колонки Excel:**
| Excel | → | БД | Обязательно? |
|------|---|-----|-------------|
| Наименование процесса | → | process_name | ✓ |
| Продукт | → | product_type | ✓ |
| Статус | → | status | ✓ |
| Дата КБ | → | date_kb | ✗ |
| ФИО | → | fio_customer | ✗ |
| Дата приемки Банк | → | date_bank_receipt | ✗ |
| ФИО от Банка | → | fio_bank_officer | ✗ |

**Пример данных:**
```
Наименование процесса | Продукт | Статус | Дата КБ | ФИО | Дата приемки Банк | ФИО от Банка
Добавление договора | Аренда Сейфов | Выполнено | 20/11/25 | Васильева Ю.С. | 4/12/25 | Половинкина
Передать/Принять ячейку | Аренда Сейфов | Выполнено | 20/11/25 | Васильева Ю.С. | 4/12/25 | Половинкина
```

**Code snippet:**
```python
# services/excel_mapper.py
SAFES_RENTAL_MAPPING = {
    'наименование процесса': 'process_name',
    'продукт': 'product_type',
    'статус': 'status',
    'дата кб': 'date_kb',
    'фио': 'fio_customer',
    'дата приемки банк': 'date_bank_receipt',
    'фио от банка': 'fio_bank_officer',
}

SAFES_RENTAL_SOURCE = 'safes_rental'
```

---

### 2️⃣ ДЕПОЗИТЫ ФЛ (deposits_fl)

**Исходные колонки Excel:**
| Excel | → | БД | Обязательно? |
|------|---|-----|-------------|
| Нпп | → | process_number | ✗ |
| Наименование процесса | → | process_name | ✓ |
| Продукт | → | product_type | ✓ |
| Статус | → | status | ✓ |
| Дата приемки | → | date_bank_receipt | ✗ |
| ФИО от Банка | → | fio_bank_officer | ✗ |
| Комментарий | → | comments | ✗ |

**Пример данных:**
```
Нпп | Наименование процесса | Продукт | Статус | Дата приемки | ФИО от Банка | Комментарий
1 | Капитализация % текущих + Учет % | Депозиты ФЛ | Успешно | | | по операционно отрабатывает корректно
2 | Учет %-капитализация (групповой обработкой) | Депозиты ФЛ | Успешно | | | не по всем вкладам отрабатывает
```

**Code snippet:**
```python
DEPOSITS_FL_MAPPING = {
    'нпп': 'process_number',
    'наименование процесса': 'process_name',
    'продукт': 'product_type',
    'статус': 'status',
    'дата приемки': 'date_bank_receipt',
    'фио от банка': 'fio_bank_officer',
    'комментарий': 'comments',
}

DEPOSITS_FL_SOURCE = 'deposits_fl'
```

---

### 3️⃣ ДЕПОЗИТЫ ЮЛ (deposits_ul)

**Исходные колонки Excel:**
| Excel | → | БД | Обязательно? |
|------|---|-----|-------------|
| Наименование процесса | → | process_name | ✓ |
| Статус | → | status | ✓ |
| Комментарий | → | comments | ✗ |

**Пример данных:**
```
Наименование процесса | Статус | Комментарий
1) открытие депозитов с отображением счетов и параметров депозита | Выполнено | 
1.1) в фактуре | | 
1.2) в АВС | Выполнено | 
```

**Code snippet:**
```python
DEPOSITS_UL_MAPPING = {
    'наименование процесса': 'process_name',
    'статус': 'status',
    'комментарий': 'comments',
}

DEPOSITS_UL_SOURCE = 'deposits_ul'
```

---

### 4️⃣ КРЕДИТЫ ФЛ (credits_fl)

**Исходные колонки Excel:**
| Excel | → | БД | Обязательно? |
|------|---|-----|-------------|
| Наименование процесса | → | process_name | ✓ |
| Продукт | → | product_type | ✓ |
| Статус | → | status | ✓ |
| Дата КБ | → | date_kb | ✗ |
| Стойбец (Стойлец) | → | bank_employee_name | ✗ |
| ФИО КБ | → | fio_bank_officer | ✗ |
| Дата приемки Банк | → | date_bank_receipt | ✗ |
| ФИО от Банка | → | fio_bank_officer | ✗ |

**Примечание:** Некоторые источники повторяют поле `fio_bank_officer`

**Code snippet:**
```python
CREDITS_FL_MAPPING = {
    'наименование процесса': 'process_name',
    'продукт': 'product_type',
    'статус': 'status',
    'дата кб': 'date_kb',
    'стойбец': 'bank_employee_name',  # может быть "Стойлец"
    'фио кб': 'fio_bank_officer',
    'дата приемки банк': 'date_bank_receipt',
    'фио от банка': 'fio_bank_officer',  # в случае конфликта — last one wins
}

CREDITS_FL_SOURCE = 'credits_fl'
```

---

### 5️⃣ ПЛАТЕЖНЫЕ ПОРУЧЕНИЯ В РУБЛЯХ (payment_orders)

**Исходные колонки Excel:**
| Excel | → | БД | Обязательно? |
|------|---|-----|-------------|
| Наименование процесса | → | process_name | ✓ |
| Продукт | → | product_type | ✓ |
| Статус | → | status | ✓ |
| Комментарий | → | comments | ✗ |

**Code snippet:**
```python
PAYMENT_ORDERS_MAPPING = {
    'наименование процесса': 'process_name',
    'продукт': 'product_type',
    'статус': 'status',
    'комментарий': 'comments',
}

PAYMENT_ORDERS_SOURCE = 'payment_orders'
```

---

### 6️⃣ ОБРАБОТКА ПЛАТЕЖЕЙ В РУБЛЯХ И ИН. ВАЛЮТЕ (payment_processing)

**Исходные колонки Excel:**
| Excel | → | БД | Обязательно? |
|------|---|-----|-------------|
| Наименование процесса | → | process_name | ✓ |
| Продукт | → | product_type | ✗ |
| Статус | → | status | ✓ |
| Комментарий | → | comments | ✗ |

**Code snippet:**
```python
PAYMENT_PROCESSING_MAPPING = {
    'наименование процесса': 'process_name',
    'продукт': 'product_type',
    'статус': 'status',
    'комментарий': 'comments',
}

PAYMENT_PROCESSING_SOURCE = 'payment_processing'
```

---

## Полный маппер (Python)

```python
# services/excel_mapper.py
from typing import Dict, Tuple
from enum import Enum

class TableSourceEnum(str, Enum):
    SAFES_RENTAL = "safes_rental"
    DEPOSITS_FL = "deposits_fl"
    DEPOSITS_UL = "deposits_ul"
    CREDITS_FL = "credits_fl"
    PAYMENT_ORDERS = "payment_orders"
    PAYMENT_PROCESSING = "payment_processing"

class StatusEnum(str, Enum):
    COMPLETED = "Выполнено"
    SUCCESS = "Успешно"
    IN_PROGRESS = "В работе"
    NOT_STARTED = "Не начато"
    FAILED = "Не успешно"

# Маппинги
COLUMN_MAPPINGS = {
    TableSourceEnum.SAFES_RENTAL: {
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'дата кб': 'date_kb',
        'фио': 'fio_customer',
        'дата приемки банк': 'date_bank_receipt',
        'фио от банка': 'fio_bank_officer',
    },
    TableSourceEnum.DEPOSITS_FL: {
        'нпп': 'process_number',
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'дата приемки': 'date_bank_receipt',
        'фио от банка': 'fio_bank_officer',
        'комментарий': 'comments',
    },
    TableSourceEnum.DEPOSITS_UL: {
        'наименование процесса': 'process_name',
        'статус': 'status',
        'комментарий': 'comments',
    },
    TableSourceEnum.CREDITS_FL: {
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'дата кб': 'date_kb',
        'стойбец': 'bank_employee_name',
        'фио кб': 'fio_bank_officer',
        'дата приемки банк': 'date_bank_receipt',
        'фио от банка': 'fio_bank_officer',
    },
    TableSourceEnum.PAYMENT_ORDERS: {
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'комментарий': 'comments',
    },
    TableSourceEnum.PAYMENT_PROCESSING: {
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'комментарий': 'comments',
    },
}

def detect_source(excel_columns: list) -> TableSourceEnum:
    """
    Автоматически определяет источник таблицы на основе набора колонок.
    """
    excel_cols_lower = [col.lower().strip() for col in excel_columns]
    
    # Детектирование по уникальным колонкам
    for source, mapping in COLUMN_MAPPINGS.items():
        required_cols = set(mapping.keys())
        if required_cols.issubset(set(excel_cols_lower)):
            return source
    
    # Fallback: угадать по наличию ключевых колонок
    if 'нпп' in excel_cols_lower:
        return TableSourceEnum.DEPOSITS_FL
    if 'стойбец' in excel_cols_lower:
        return TableSourceEnum.CREDITS_FL
    
    raise ValueError(f"Cannot detect table source from columns: {excel_columns}")

def map_excel_row_to_record(row_data: dict, source: TableSourceEnum) -> dict:
    """
    Маппирует данные из Excel строки в структуру ProcessRecord.
    
    Args:
        row_data: dict с исходными данными из Excel
        source: определённый источник таблицы
    
    Returns:
        dict готовый для создания ProcessRecord
    """
    mapping = COLUMN_MAPPINGS[source]
    result = {
        'table_source': source.value,
    }
    
    # Маппирование каждого поля
    for excel_col, db_field in mapping.items():
        if excel_col in row_data:
            value = row_data[excel_col]
            
            # Парсинг даты
            if 'date' in db_field and value:
                value = parse_date(value)
            
            result[db_field] = value or None
    
    return result

def parse_date(date_str) -> str:
    """
    Парсит дату из различных форматов.
    Возвращает строку в формате YYYY-MM-DD для БД.
    """
    from datetime import datetime
    
    if isinstance(date_str, str):
        # Пробуем различные форматы
        formats = ['%d/%m/%y', '%d.%m.%y', '%Y-%m-%d', '%d/%m/%Y']
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        raise ValueError(f"Cannot parse date: {date_str}")
    
    # Если уже datetime объект
    return date_str.strftime('%Y-%m-%d')
```

---

## Валидация данных

```python
# services/validation.py
from typing import Tuple, List

class ValidationError:
    def __init__(self, row: int, field: str, message: str):
        self.row = row
        self.field = field
        self.message = message
    
    def __repr__(self):
        return f"Row {self.row}, Field '{self.field}': {self.message}"

def validate_record(data: dict, source: str) -> Tuple[bool, List[ValidationError]]:
    """
    Валидирует одну запись перед сохранением.
    """
    errors = []
    
    # Обязательные поля
    if not data.get('process_name') or not str(data['process_name']).strip():
        errors.append(ValidationError(0, 'process_name', 'Required field'))
    
    if not data.get('status') or data['status'] not in StatusEnum.__members__.values():
        valid_statuses = [e.value for e in StatusEnum]
        errors.append(ValidationError(
            0, 'status', 
            f"Must be one of: {', '.join(valid_statuses)}"
        ))
    
    # Валидация дат
    for date_field in ['date_kb', 'date_bank_receipt']:
        if data.get(date_field):
            try:
                parse_date(data[date_field])
            except ValueError as e:
                errors.append(ValidationError(0, date_field, str(e)))
    
    return len(errors) == 0, errors
```

---

## Пример использования в API

```python
# api/import_excel.py
from fastapi import APIRouter, UploadFile, File
from services.excel_mapper import detect_source, map_excel_row_to_record
from services.validation import validate_record
import openpyxl

router = APIRouter()

@router.post("/import/excel")
async def import_excel(file: UploadFile = File(...)):
    """
    Импортирует данные из Excel файла.
    """
    import_batch_id = generate_batch_id()
    errors = []
    success_count = 0
    
    # Парсим Excel
    wb = openpyxl.load_workbook(file.file)
    ws = wb.active
    
    # Получаем заголовки
    headers = [cell.value for cell in ws[1]]
    
    # Детектируем источник
    try:
        source = detect_source(headers)
    except ValueError as e:
        return {"error": str(e), "status": 400}
    
    # Обрабатываем строки
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        row_data = {h: row[i] for i, h in enumerate(headers) if h}
        
        # Маппируем
        record_data = map_excel_row_to_record(row_data, source)
        
        # Валидируем
        is_valid, validation_errors = validate_record(record_data, source.value)
        
        if not is_valid:
            for err in validation_errors:
                err.row = row_idx
                errors.append(err)
            continue
        
        # Сохраняем в БД
        db.add(ProcessRecord(**record_data))
        success_count += 1
    
    db.commit()
    
    # Логируем импорт
    log_entry = ImportLog(
        import_batch_id=import_batch_id,
        filename=file.filename,
        table_source=source.value,
        total_rows=ws.max_row - 1,
        success_rows=success_count,
        error_rows=len(errors),
        error_details=[asdict(e) for e in errors],
    )
    db.add(log_entry)
    db.commit()
    
    return {
        "import_batch_id": import_batch_id,
        "success_rows": success_count,
        "error_rows": len(errors),
        "errors": [asdict(e) for e in errors[:10]],  # Показываем первые 10
    }
```

---

## Таблица соответствия статусов

| Русский | Value в БД | Color |
|--------|-----------|-------|
| Выполнено | Выполнено | 🟩 Зелёный |
| Успешно | Успешно | 🟩 Зелёный |
| В работе | В работе | 🟨 Жёлтый |
| Не начато | Не начато | ⬜ Серый |
| Не успешно | Не успешно | 🔴 Красный (опционально) |

---

## Дополнительные примеры

### Пример Excel файла (CSV для тестирования)

```csv
Наименование процесса,Продукт,Статус,Дата КБ,ФИО,Дата приемки Банк,ФИО от Банка
Добавление договора,Аренда Сейфов,Выполнено,20/11/25,Васильева Ю.С.,4/12/25,Половинкина
Передать/Принять ячейку,Аренда Сейфов,Выполнено,20/11/25,Васильева Ю.С.,4/12/25,Половинкина
Вскрытие сейфа,Аренда Сейфов,Выполнено,20/11/25,Васильева Ю.С.,9/12/25,Половинкина
```

### SQL для проверки импортированных данных

```sql
-- Проверить по источнику
SELECT table_source, COUNT(*) as total, 
       SUM(CASE WHEN status = 'Выполнено' THEN 1 ELSE 0 END) as completed
FROM process_records
GROUP BY table_source;

-- Проверить последний импорт
SELECT * FROM import_logs 
ORDER BY imported_at DESC 
LIMIT 1;

-- Посмотреть ошибки
SELECT * FROM import_logs 
WHERE error_rows > 0 
ORDER BY imported_at DESC;
```

---

**Дата:** 12 декабря 2025  
**Версия:** 1.0
