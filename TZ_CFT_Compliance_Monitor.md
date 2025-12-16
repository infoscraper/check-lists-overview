# Техническая Спецификация
## Система мониторинга прогресса процессов "Compliance Program" ЦФТ-Банк

---

## 1. Краткое описание проекта

**Название:** Compliance Progress Monitor (CPM)

**Цель:** Создать веб-приложение для визуализации и управления прогрессом тестирования операций в ЦФТ-Банк с возможностью импорта данных из Excel, ручного редактирования таблиц и отслеживания статусов в режиме реального времени.

**Целевые пользователи:** Аналитики, менеджеры качества и контроля, сотрудники compliance-отдела.

**Основная ценность:** Единое место для просмотра и управления прогрессом тестирования, автоматизированный импорт данных, визуальная демонстрация статусов (dashboard).

**Платформа:** Web-приложение (SPA), кроссбраузерное.

---

## 2. Scope

### In Scope

- ✅ Dashboard с обзором прогресса (кол-во выполненных, в работе, не начато)
- ✅ Вкладка "Детализация чек-листов" с таблицами для каждого источника (6 таблиц)
- ✅ Визуализация прогресса как сетка квадратиков (каждый квадратик = строка данных)
- ✅ Статусы: серая (не начато), желтая (в работе), зеленая (выполнено)
- ✅ Импорт данных из Excel файлов (маппинг по унифицированной схеме)
- ✅ CRUD операции (просмотр, добавление, редактирование, удаление строк)
- ✅ Сохранение данных в БД
- ✅ Экспорт текущих данных обратно в Excel

### Out of Scope

- ❌ Multi-user роли и permissions (администратор/пользователь)
- ❌ Версионирование истории изменений
- ❌ Email-уведомления о статусах
- ❌ Генерация отчётов в PDF
- ❌ Mobile-приложение (только десктоп/планшет)
- ❌ API для интеграции с другими системами

---

## 3. Предположения и ограничения

| Категория | Значение |
|-----------|----------|
| **Язык документов** | Русский |
| **Языки кода** | Python (backend), TypeScript/JavaScript (frontend) |
| **Фреймворк backend** | FastAPI |
| **ОRM** | SQLAlchemy + Alembic (миграции) |
| **БД** | PostgreSQL 14+ |
| **Frontend фреймворк** | React 18+ + TypeScript |
| **UI библиотека** | Shadcn/ui (или Material-UI) |
| **Формат импорта** | .xlsx (Excel), маппинг по унифицированной схеме из п. 1 |
| **Объём данных** | ~5000 строк на начальном этапе, масштабируется до 50k |
| **Одновременные пользователи** | 1–10 (учебный / внутренний проект) |
| **Окружение** | Docker Compose (локальное / на сервере) |
| **Сроки** | ~3–4 недели разработки |
| **Бюджет** | Open source стеки, без платных сервисов |

---

## 4. User Flows

1. **Открыть приложение → Dashboard**
   - Пользователь видит обзор: общий прогресс (73% = 65/89), кол-во чек-листов (8 controls), выполнено (16/33).
   - Визуально: 2 блока с сетками прогресса (наподобие скрина).

2. **Перейти на вкладку "Детализация чек-листов"**
   - Система выводит табы/вкладки для каждого источника (Аренда Сейфов, Депозиты ФЛ, и т.д.).
   - Каждая таблица содержит колонки согласно унифицированной схеме (п. 1.1).

3. **Импортировать Excel файл**
   - Пользователь выбирает файл .xlsx → система парсит лист → маппит колонки по унифицированной схеме.
   - Автоматически заполняются соответствующие таблицы (по `table_source`).
   - Отображается статус импорта (успех / ошибки валидации).

4. **Просмотреть и отредактировать таблицу**
   - Пользователь видит таблицу с колонками.
   - Клик на ячейку → редактирование inline или модальное окно.
   - Сохранение при смене фокуса или нажатии "Сохранить".

5. **Добавить новую строку**
   - Кнопка "Добавить запись" → открывается форма/модальное окно.
   - Заполнение полей → "Сохранить" → строка добавляется в таблицу и БД.

6. **Удалить строку**
   - Каждая строка имеет кнопку "Удалить" или чекбокс → "Удалить выбранные".
   - Подтверждение удаления → строки удаляются.

7. **Экспортировать данные**
   - Кнопка "Экспортировать в Excel" → скачивание файла со всеми текущими данными.

---

## 5. Функциональные требования

### Модуль 1: Dashboard (обзор прогресса)

| ID | Описание | Приоритет |
|----|----------|-----------|
| **F1.1** | Отображение карточки "Общий прогресс" с процентом выполнения (65/89 = 73%) | **Must** |
| **F1.2** | Отображение двух блоков-сеток (как на скрине): по 2 сетки с квадратиками, каждый квадратик соответствует одной строке данных | **Must** |
| **F1.3** | Квадратик зелёный, если статус = "Выполнено"/"Успешно", жёлтый = "В работе", серый = "Не начато" | **Must** |
| **F1.4** | Tooltip на наведении на квадратик: показать процесс_name, статус, дату | **Should** |
| **F1.5** | Обновление dashboard при изменении данных (без перезагрузки страницы) | **Should** |

### Модуль 2: Детализация чек-листов (таблицы)

| ID | Описание | Приоритет |
|----|----------|-----------|
| **F2.1** | Наличие вкладок/табов для каждого источника: Аренда Сейфов, Депозиты ФЛ, Депозиты ЮЛ, Кредиты ФЛ, Платежные поручения, Обработка платежей | **Must** |
| **F2.2** | Каждая таблица содержит столбцы согласно унифицированной схеме (п. 1.1): process_name, product_type, status, date_kb, fio_customer, date_bank_receipt, fio_bank_officer, process_number, bank_employee_name, comments | **Must** |
| **F2.3** | Пустые поля (NULL) отображаются как пустые ячейки или "--" | **Should** |
| **F2.4** | Сортировка таблицы по любому столбцу (ASC/DESC) | **Should** |
| **F2.5** | Фильтрация по статусу, product_type, дате | **Should** |
| **F2.6** | Поиск по process_name (substring search) | **Should** |

### Модуль 3: Импорт данных из Excel

| ID | Описание | Приоритет |
|----|----------|-----------|
| **F3.1** | Кнопка "Импортировать Excel" на главной / в каждой вкладке | **Must** |
| **F3.2** | Выбор файла .xlsx → система парсит первый лист (или выбранный лист) | **Must** |
| **F3.3** | Маппинг колонок исходного Excel на унифицированную схему (по названиям колонок, case-insensitive) | **Must** |
| **F3.4** | Детектирование source таблицы на основе набора колонок или явного указания пользователем | **Must** |
| **F3.5** | Валидация данных перед импортом (обязательные поля, типы данных, формат дат) | **Must** |
| **F3.6** | Отображение ошибок валидации с указанием строки и поля | **Must** |
| **F3.7** | Опция "Заменить существующие данные" vs "Добавить новые" (с дедупликацией по process_name + product_type) | **Should** |
| **F3.8** | Логирование импорта с batch_id и кол-вом загруженных записей | **Should** |

### Модуль 4: CRUD операции (таблицы)

| ID | Описание | Приоритет |
|----|----------|-----------|
| **F4.1** | Inline редактирование ячеек (двойной клик или специальная кнопка "Edit") | **Must** |
| **F4.2** | Валидация при редактировании (типы, обязательные поля) | **Must** |
| **F4.3** | Автосохранение при смене фокуса (debounce 500ms) | **Should** |
| **F4.4** | Кнопка "Добавить запись" → открывает форму/модальное окно с пустыми полями | **Must** |
| **F4.5** | Кнопка "Удалить" на каждой строке → подтверждение → удаление | **Must** |
| **F4.6** | Bulk delete (выделение нескольких строк чекбоксами → удаление) | **Should** |
| **F4.7** | Отмена операции (Ctrl+Z / кнопка "Отмена") — откат последнего изменения | **Could** |

### Модуль 5: Экспорт данных

| ID | Описание | Приоритет |
|----|----------|-----------|
| **F5.1** | Кнопка "Экспортировать в Excel" → скачивание файла со всеми текущими данными | **Should** |
| **F5.2** | Экспорт включает все строки и колонки текущей вкладки (или глобального экспорта для всех таблиц) | **Should** |
| **F5.3** | Форматирование Excel (заголовки, ширина колонок, автофильтр) | **Could** |

---

## 6. Data Model (структура БД)

### Таблица: `process_records`

```sql
CREATE TABLE process_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Основные данные процесса
    process_name VARCHAR(255) NOT NULL,
    product_type VARCHAR(100),
    status VARCHAR(50) NOT NULL CHECK (status IN ('Выполнено', 'Успешно', 'В работе', 'Не начато', 'Не успешно')),
    
    -- Даты и лица
    date_kb DATE,
    fio_customer VARCHAR(255),
    date_bank_receipt DATE,
    fio_bank_officer VARCHAR(255),
    
    -- Доп. поля
    process_number INT,
    bank_employee_name VARCHAR(255),
    comments TEXT,
    
    -- Служебные
    table_source VARCHAR(100) NOT NULL CHECK (table_source IN (
        'safes_rental',
        'deposits_fl',
        'deposits_ul',
        'credits_fl',
        'payment_orders',
        'payment_processing'
    )),
    import_date TIMESTAMP DEFAULT NOW(),
    import_batch_id VARCHAR(100),
    is_archived BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Индексы
CREATE INDEX idx_process_records_status ON process_records(status);
CREATE INDEX idx_process_records_table_source ON process_records(table_source);
CREATE INDEX idx_process_records_import_batch ON process_records(import_batch_id);
CREATE INDEX idx_process_records_process_name ON process_records(process_name);
```

### Таблица: `import_logs`

```sql
CREATE TABLE import_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    import_batch_id VARCHAR(100) NOT NULL UNIQUE,
    filename VARCHAR(255),
    table_source VARCHAR(100),
    total_rows INT,
    success_rows INT,
    error_rows INT,
    error_details JSONB,
    imported_at TIMESTAMP DEFAULT NOW(),
    imported_by VARCHAR(255)
);
```

---

## 7. API Contract

### Endpoints

| Метод | Path | Описание | Auth | Ошибки |
|-------|------|---------|------|--------|
| **GET** | `/api/dashboard/summary` | Получить сводку: % прогресса, кол-во по статусам | - | 500 |
| **GET** | `/api/records` | Получить все записи (с фильтром `table_source`, `status`) | - | 400, 500 |
| **GET** | `/api/records/{id}` | Получить одну запись | - | 404, 500 |
| **POST** | `/api/records` | Создать новую запись | - | 400, 422, 500 |
| **PUT** | `/api/records/{id}` | Обновить запись | - | 404, 400, 422, 500 |
| **DELETE** | `/api/records/{id}` | Удалить запись | - | 404, 500 |
| **POST** | `/api/records/bulk-delete` | Удалить несколько записей (массив ID) | - | 400, 500 |
| **POST** | `/api/import/excel` | Загрузить Excel файл (multipart/form-data) | - | 400, 415, 422, 500 |
| **GET** | `/api/import/logs` | Получить историю импортов | - | 500 |
| **GET** | `/api/export/excel` | Скачать Excel со всеми данными (или по `table_source`) | - | 500 |

### Примеры запросов/ответов

#### POST `/api/records`
```json
Request:
{
  "process_name": "Добавление договора",
  "product_type": "Аренда Сейфов",
  "status": "Выполнено",
  "date_kb": "2025-12-04",
  "fio_customer": "Иванов И.И.",
  "table_source": "safes_rental"
}

Response (201):
{
  "id": "uuid-xxx",
  "process_name": "Добавление договора",
  "product_type": "Аренда Сейфов",
  "status": "Выполнено",
  "table_source": "safes_rental",
  "created_at": "2025-12-12T10:30:00Z"
}
```

#### POST `/api/import/excel`
```json
Request: multipart/form-data
- file: <binary xlsx>

Response (202):
{
  "import_batch_id": "batch_20251212_001",
  "total_rows": 45,
  "success_rows": 43,
  "error_rows": 2,
  "errors": [
    {
      "row": 5,
      "field": "status",
      "message": "Invalid status value"
    }
  ]
}
```

#### GET `/api/dashboard/summary`
```json
Response (200):
{
  "total_records": 89,
  "completed": 65,
  "in_progress": 15,
  "not_started": 9,
  "progress_percent": 73,
  "by_source": {
    "safes_rental": { "total": 10, "completed": 9, "in_progress": 1 },
    "deposits_fl": { "total": 25, "completed": 16, "in_progress": 5, "not_started": 4 }
  }
}
```

---

## 8. Non-Functional Requirements

| Требование | Значение |
|------------|----------|
| **Производительность** | Загрузка страницы < 2с, импорт 1000 строк < 5с |
| **Масштабируемость** | До 50k записей без деградации (индексы на status, table_source) |
| **Доступность** | 99.5% uptime для локального сервера |
| **Безопасность** | Input validation, SQL injection prevention (ORM), CSRF tokens, no secrets in logs |
| **Логирование** | Все операции CRUD, импорты, ошибки → файл/stdout, level: INFO |
| **Кэширование** | Redis для dashboard summary (TTL 5 мин), или in-memory cache |
| **Валидация** | На backend: обязательные поля, типы данных, формат дат (YYYY-MM-DD) |
| **Браузеры** | Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ |
| **Ответственность API** | < 100ms для GET без фильтра, < 500ms с фильтром |

---

## 9. Architecture (высокоуровневая)

### Диаграмма компонентов

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (React 18 + TS)                      │
├──────────────────────────────────────────────────────────────────┤
│  - Dashboard (обзор с сетками)                                   │
│  - Tabs: Детализация чек-листов (6 таблиц)                       │
│  - Modal: Add/Edit Record                                         │
│  - Import Dialog (Excel upload)                                   │
│  - Export Button                                                  │
└────────┬─────────────────────────────────────────────────────────┘
         │ (REST API)
         │
┌────────▼─────────────────────────────────────────────────────────┐
│                  Backend API (FastAPI + Python)                   │
├──────────────────────────────────────────────────────────────────┤
│  - GET /api/dashboard/summary                                    │
│  - GET/POST/PUT/DELETE /api/records                              │
│  - POST /api/import/excel (парсинг + маппинг)                    │
│  - GET /api/export/excel                                          │
│  - POST /api/records/bulk-delete                                 │
└────────┬─────────────────────────────────────────────────────────┘
         │ (SQLAlchemy ORM)
         │
┌────────▼─────────────────────────────────────────────────────────┐
│              Database (PostgreSQL 14+)                            │
├──────────────────────────────────────────────────────────────────┤
│  - process_records (главная таблица)                              │
│  - import_logs (логирование импортов)                             │
└──────────────────────────────────────────────────────────────────┘
```

### Стек технологий

| Слой | Технология | Версия |
|------|-----------|--------|
| **Backend** | Python | 3.11+ |
| **Web Framework** | FastAPI | 0.104+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **DB Migrations** | Alembic | 1.12+ |
| **Database** | PostgreSQL | 14+ |
| **Frontend** | React | 18+ |
| **Type Safety** | TypeScript | 5+ |
| **UI Components** | Shadcn/ui | latest |
| **HTTP Client** | axios / fetch | - |
| **Excel Parsing** | openpyxl (backend) | 3.10+ |
| **Excel Export** | python-xlsx / openpyxl | 3.10+ |
| **Containerization** | Docker + Docker Compose | latest |

### Структура папок

```
project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # конфиги, env vars
│   │   ├── models/
│   │   │   └── process_record.py      # SQLAlchemy models
│   │   ├── schemas/
│   │   │   └── record_schema.py       # Pydantic schemas
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── records.py             # CRUD endpoints
│   │   │   ├── dashboard.py           # summary endpoint
│   │   │   ├── import_excel.py        # импорт из Excel
│   │   │   └── export.py              # экспорт в Excel
│   │   ├── services/
│   │   │   ├── record_service.py      # бизнес-логика CRUD
│   │   │   ├── excel_mapper.py        # маппинг колонок, парсинг
│   │   │   └── excel_exporter.py      # экспорт
│   │   └── db/
│   │       ├── database.py            # подключение к БД
│   │       └── session.py             # сессия управление
│   ├── migrations/                    # Alembic миграции
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── TableView.tsx
│   │   │   ├── ImportDialog.tsx
│   │   │   ├── RecordModal.tsx
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── MainPage.tsx
│   │   │   └── DetailPage.tsx
│   │   ├── api/
│   │   │   └── client.ts              # axios instance + API calls
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript interfaces
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## 10. Development Plan (последовательность реализации)

### M1: Environment & Skeleton (1–2 дня)

- [ ] Инициализация backend: FastAPI boilerplate, структура папок
- [ ] Инициализация frontend: React + TypeScript + Vite
- [ ] Docker Compose с PostgreSQL
- [ ] Environment variables (.env.example)
- [ ] Git репозиторий, базовый README
- **Deliverable:** Оба сервера стартуют без ошибок, БД доступна

### M2: Database & Models (2–3 дня)

- [ ] Создание Alembic migrations
- [ ] Создание SQLAlchemy моделей (process_records, import_logs)
- [ ] Создание индексов
- [ ] Создание Pydantic schemas для CRUD
- [ ] Инициализация алембик для миграций
- **Deliverable:** `alembic upgrade head` создает таблицы, миграции работают

### M3: Backend CRUD API (3–4 дня)

- [ ] Реализация endpoints: GET /api/records, POST, PUT, DELETE
- [ ] Валидация в schemas и в модельных ограничениях
- [ ] Error handling (404, 422, 500)
- [ ] Фильтрация и сортировка в GET /api/records
- [ ] Логирование операций
- [ ] Unit тесты для CRUD (pytest)
- **Deliverable:** Все CRUD endpoints работают, тесты проходят

### M4: Excel Импорт (4–5 дней)

- [ ] Реализация парсера Excel (openpyxl)
- [ ] Маппинг колонок по унифицированной схеме
- [ ] Валидация данных перед вставкой (format check, null check)
- [ ] Создание import_logs записей
- [ ] Error reporting (какие строки / поля не валидны)
- [ ] Endpoint POST /api/import/excel
- [ ] Обработка дедупликации (если нужно)
- **Deliverable:** Тестовый Excel файл загружается, данные в БД, ошибки отображаются корректно

### M5: Dashboard Backend (2–3 дня)

- [ ] Реализация GET /api/dashboard/summary (агрегация по статусам)
- [ ] Кэширование результатов (in-memory или Redis)
- [ ] Группировка по table_source
- [ ] Тесты для расчетов
- **Deliverable:** Endpoint возвращает корректные % и кол-во по статусам

### M6: Frontend Dashboard (4–5 дней)

- [ ] Компонент Dashboard: отображение карточек обзора
- [ ] Сетка квадратиков (grid layout, CSS) с цветовыми кодами
- [ ] Tooltip при наведении
- [ ] Интеграция с API (axios call, useEffect)
- [ ] Обновление при изменении данных (polling или websocket, опционально)
- [ ] Responsive дизайн
- **Deliverable:** Dashboard отображает % прогресса и сетки квадратиков

### M7: Frontend Таблицы (5–6 дней)

- [ ] Компонент TableView: отображение таблиц с колонками
- [ ] Таб-система для 6 источников (Arenда, Депозиты и т.д.)
- [ ] Inline редактирование (двойной клик, autosave debounce)
- [ ] Сортировка и фильтрация (UI)
- [ ] Отправка фильтров на backend (GET параметры)
- [ ] Отображение пустых полей
- **Deliverable:** Все 6 таблиц отображаются, редактирование работает

### M8: Frontend CRUD UI (3–4 дня)

- [ ] Модальное окно для добавления записи (форма с валидацией)
- [ ] Модальное окно для редактирования (предзаполнение)
- [ ] Кнопка "Удалить" с подтверждением
- [ ] Bulk delete (чекбоксы)
- [ ] Toast-уведомления об успехе/ошибке
- **Deliverable:** CRUD операции работают, ошибки выводятся пользователю

### M9: Frontend Импорт (3–4 дня)

- [ ] Dialog для выбора файла
- [ ] Drag-and-drop зона для файла
- [ ] Progress bar при загрузке
- [ ] Отображение результатов (success / errors)
- [ ] Опция "Заменить" vs "Добавить"
- [ ] Интеграция с backend импортом
- **Deliverable:** Файл .xlsx загружается, таблицы заполняются, ошибки видны

### M10: Экспорт (2 дня)

- [ ] Backend: реализация exporter (openpyxl или python-xlsx)
- [ ] Форматирование Excel (заголовки, ширина колонок, фильтр)
- [ ] Endpoint GET /api/export/excel
- [ ] Frontend: кнопка "Экспортировать", скачивание файла
- **Deliverable:** Кнопка экспорта скачивает .xlsx со всеми данными

### M11: Тестирование & Баги (4–5 дней)

- [ ] E2E тесты (Cypress / Playwright): основные сценарии
- [ ] Integration тесты: импорт + проверка данных
- [ ] Баг-фиксинг, оптимизация
- [ ] Проверка на браузерах
- **Deliverable:** Все тесты проходят, критические баги закрыты

### M12: Документация & Деплой (2–3 дня)

- [ ] API documentation (Swagger/OpenAPI)
- [ ] README: установка, запуск, использование
- [ ] Dockerfile оптимизация
- [ ] Инструкция по развертыванию (локально, на сервере)
- [ ] Проверка переменных окружения
- **Deliverable:** Полная документация, приложение готово к использованию

---

## 11. Testing & Acceptance Criteria

### Feature: Dashboard Overview

**AC 1.1:** При загрузке страницы отображается карточка "Общий прогресс" с % выполнения (вычисляется как завершённые / всего * 100).

**AC 1.2:** Две сетки квадратиков, каждый квадратик соответствует одной строке процесса. Цвет квадратика зелёный (Выполнено), жёлтый (В работе), серый (Не начато).

**AC 1.3:** При наведении курсора на квадратик показывается tooltip с process_name, статусом, датой.

**Test Case:**
```python
def test_dashboard_summary_calculation():
    # 65 completed из 89 = 73%
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    assert response.json()["progress_percent"] == 73
    assert response.json()["completed"] == 65
```

### Feature: Excel Import

**AC 3.1:** Выбор файла .xlsx → система парсит первый лист и маппит колонки.

**AC 3.2:** Все строки валидны → все добавляются в БД, возвращается success (200/202).

**AC 3.3:** Если есть ошибки валидации (неправильный статус, неправильная дата) → возвращается список ошибок с row номер и field.

**Test Case:**
```python
def test_import_excel_valid():
    with open("test_data.xlsx", "rb") as f:
        response = client.post(
            "/api/import/excel",
            files={"file": f}
        )
    assert response.status_code == 202
    assert response.json()["success_rows"] == 45
```

### Feature: CRUD Operations

**AC 4.1:** Добавление новой записи → все обязательные поля заполнены → запись в БД.

**AC 4.2:** Редактирование ячейки → при смене фокуса сохранение (debounce 500ms) → без ошибок.

**AC 4.3:** Удаление записи → подтверждение → запись из БД удаляется.

**Test Case:**
```python
def test_create_record():
    data = {
        "process_name": "Test Process",
        "status": "Выполнено",
        "table_source": "safes_rental"
    }
    response = client.post("/api/records", json=data)
    assert response.status_code == 201
    assert response.json()["id"] is not None
```

### Unit Tests

- `test_models.py`: проверка constraints, валидации на уровне БД
- `test_schemas.py`: Pydantic валидация
- `test_excel_mapper.py`: маппинг колонок, парсинг даты
- `test_api.py`: все endpoints (CRUD, импорт, export)

### Integration Tests

- `test_import_to_ui.py`: загрузить Excel → проверить UI отражает данные
- `test_crud_flow.py`: создать → отредактировать → удалить

### E2E Tests (Cypress/Playwright)

- Открыть приложение → Dashboard видна
- Перейти на вкладку → таблица видна
- Импортировать файл → данные заполняются
- Отредактировать строку → сохранение работает
- Удалить строку → таблица обновляется
- Экспортировать → файл скачивается

---

## 12. Deployment & Operations

### Docker Compose

```yaml
version: '3.9'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: compliance
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: compliance_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://compliance:${DB_PASSWORD}@postgres:5432/compliance_db
      ENVIRONMENT: ${ENVIRONMENT}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      VITE_API_BASE_URL: http://localhost:8000

volumes:
  postgres_data:
```

### Environment Variables

```
# .env.example
ENVIRONMENT=development
DB_PASSWORD=securepassword123
DATABASE_URL=postgresql://compliance:securepassword123@postgres:5432/compliance_db
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
CACHE_TTL=300
```

### Миграции БД

```bash
# Создание миграции
alembic revision --autogenerate -m "Initial migration"

# Применение миграций
alembic upgrade head

# Откат
alembic downgrade -1
```

### Логирование

```python
import logging
logger = logging.getLogger(__name__)

# При импорте
logger.info(f"Import started: batch_id={batch_id}, file={filename}")
logger.error(f"Validation failed: row={row}, field={field}, error={error}")
```

### Мониторинг

- **Логи:** stdout + файл (в /var/log/)
- **Метрики:** кол-во запросов, средний response time
- **Алерты:** ошибки импорта, DB connection timeout

---

## 13. Risks & Edge Cases

| Риск | Вероятность | Impact | Mitigation |
|------|-----------|--------|-----------|
| Excel файл с неправильной структурой колонок | High | Medium | Валидация схемы, подробные error messages |
| Дублирование записей при импорте | Medium | Medium | Дедупликация по process_name + table_source, transaction rollback |
| Race condition при одновременном редактировании | Low | Medium | Optimistic locking (версионирование) или pessimistic lock |
| Большой файл Excel (10k+ строк) → timeout | Medium | Low | Асинхронная обработка (Celery), progress tracking |
| Потеря соединения с БД | Low | High | Connection pooling, retry logic, graceful error message |
| Некорректный формат даты в Excel | High | Low | Гибкое парсирование (try multiple formats), ошибка валидации |

### Edge Cases

1. **Пустое значение в обязательном поле** → ошибка валидации, выводится "This field is required"
2. **Статус не из enum** → ошибка валидации, перечень допустимых значений
3. **Дата в будущем** → сохраняется, но можно добавить warning
4. **Очень длинный текст в comments** → обрезается или выводится с scroll
5. **Попытка удалить несуществующую запись** → 404 Not Found
6. **Импорт файла с одинаковыми строками** → складываются в одну или создаются все (зависит от бизнес-логики)

---

## 14. Context7 Checklist (Verification Items)

[Context7] Следующие детали нужно уточнить в документации:

- [ ] **FastAPI dependency injection** — как работает Depends(), когда использовать (для DB session, auth)
  - Lookup: https://docs.fastapi.com/en/latest/advanced/dependency-injection/
- [ ] **SQLAlchemy relationship & cascade delete** — настройка каскадного удаления (если нужно)
  - Lookup: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
- [ ] **Alembic auto-migration** — как работает `--autogenerate`, когда вручную писать версии
  - Lookup: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- [ ] **Pydantic v2 validators** — использование @field_validator для custom validation
  - Lookup: https://docs.pydantic.dev/latest/api/validators/
- [ ] **openpyxl reading/writing** — чтение merged cells, форматирование при экспорте
  - Lookup: https://openpyxl.readthedocs.io/en/stable/
- [ ] **React useCallback & useMemo** — оптимизация компонентов при частых перерендерах (таблица)
  - Lookup: https://react.dev/reference/react/useCallback
- [ ] **Shadcn/ui Table component** — встроенная сортировка/фильтрация
  - Lookup: https://ui.shadcn.com/docs/components/data-table
- [ ] **Axios interceptors** — обработка 401/403 errors, добавление headers
  - Lookup: https://axios-http.com/docs/interceptors
- [ ] **Docker Compose networking** — как сервисы общаются между собой (backend → postgres)
  - Lookup: https://docs.docker.com/compose/networking/
- [ ] **PostgreSQL JSONB type** — использование для хранения ошибок импорта, query примеры
  - Lookup: https://www.postgresql.org/docs/15/datatype-json.html

---

## 15. Open Questions

1. **Авторизация?** На данный момент ТЗ не включает аутентификацию (public). Нужна ли?
2. **История версий?** Нужно ли хранить историю изменений каждой записи (для отката)?
3. **Асинхронный импорт?** Если файлы станут очень большие (50k+ строк), нужна ли асинхронная обработка с Celery?
4. **Webhook notifications?** Уведомления при завершении импорта (email, Slack)?
5. **Multiple sheets в одном Excel?** Поддержка нескольких листов в одном файле?
6. **Backup стратегия?** Как часто резервировать БД?

---

## Дополнительные ресурсы

- **OpenAPI/Swagger UI:** будет доступна на `http://localhost:8000/docs`
- **API тестирование:** используем Postman/Insomnia либо встроенный swagger
- **Локальный запуск:** `docker-compose up`, фронтенд на `http://localhost:3000`, API на `http://localhost:8000`

---

**Версия ТЗ:** 1.0  
**Дата:** 12 декабря 2025  
**Автор:** Architecture Team  
**Статус:** ✅ Ready for Development
