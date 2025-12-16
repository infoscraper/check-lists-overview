# 📊 Compliance Progress Monitor — Краткий обзор

## Что это?
Веб-приложение для **визуализации и управления прогрессом** тестирования операций в ЦФТ-Банк с импортом из Excel, редактированием и отслеживанием статусов.

---

## 🎯 Ключевые функции

### 1️⃣ **Dashboard (обзор прогресса)**
- Отображение % выполнения (73% = 65/89)
- Две сетки с квадратиками (каждый = одна строка процесса)
- Цвета: 🟩 зелёный (Выполнено), 🟨 жёлтый (В работе), ⬜ серый (Не начато)
- Tooltip при наведении

### 2️⃣ **Детализация чек-листов (6 таблиц)**
Каждая таблица для источника данных:
- Аренда Сейфов
- Депозиты ФЛ
- Депозиты ЮЛ
- Кредиты ФЛ
- Платежные поручения
- Обработка платежей

**Колонки (унифицированные):** process_name, product_type, status, date_kb, fio_customer, date_bank_receipt, fio_bank_officer, process_number, bank_employee_name, comments

### 3️⃣ **Импорт из Excel**
- Загрузка .xlsx файлов
- Автоматическое маппирование колонок
- Валидация данных (статусы, даты)
- Отображение ошибок с указанием строк
- Логирование импортов

### 4️⃣ **CRUD операции**
- ✏️ Редактирование ячеек (inline, autosave)
- ➕ Добавление новых записей (форма/модаль)
- 🗑️ Удаление (с подтверждением, bulk delete)
- 📊 Сортировка, фильтрация, поиск

### 5️⃣ **Экспорт в Excel**
- Скачивание всех данных в .xlsx
- Форматирование заголовков и колонок

---

## 🏗️ Tech Stack

| Слой | Технология |
|------|-----------|
| **Backend** | Python 3.11+ / FastAPI |
| **Database** | PostgreSQL 14+ |
| **ORM** | SQLAlchemy 2.0 + Alembic |
| **Frontend** | React 18 + TypeScript |
| **UI** | Shadcn/ui |
| **Excel** | openpyxl |
| **Containerization** | Docker Compose |

---

## 📁 Структура БД

### Таблица: `process_records`
```
id (UUID)
├─ process_name (VARCHAR, NOT NULL)
├─ product_type (VARCHAR)
├─ status (VARCHAR: Выполнено/Успешно/В работе/Не начато)
├─ date_kb, fio_customer, date_bank_receipt, fio_bank_officer (dates/names)
├─ process_number, bank_employee_name (опционально)
├─ comments (TEXT)
├─ table_source (enum: safes_rental, deposits_fl, deposits_ul, credits_fl, payment_orders, payment_processing)
├─ import_batch_id, import_date
└─ is_archived, created_at, updated_at
```

### Таблица: `import_logs`
Логирование всех импортов с ошибками (JSONB)

---

## 🔌 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/api/dashboard/summary` | Сводка прогресса (%, кол-во по статусам) |
| GET | `/api/records` | Получить записи (с фильтром, сортировкой) |
| POST | `/api/records` | Создать новую запись |
| PUT | `/api/records/{id}` | Обновить запись |
| DELETE | `/api/records/{id}` | Удалить запись |
| POST | `/api/records/bulk-delete` | Удалить несколько |
| POST | `/api/import/excel` | Импортировать Excel |
| GET | `/api/import/logs` | История импортов |
| GET | `/api/export/excel` | Скачать Excel со всеми данными |

---

## 📅 Plan (12 этапов, ~4 недели)

| Этап | Задача | Дней |
|------|--------|------|
| M1 | Environment setup, Docker, структура | 1-2 |
| M2 | Database models, Alembic migrations | 2-3 |
| M3 | Backend CRUD API + тесты | 3-4 |
| M4 | Excel импорт (парсер + маппинг) | 4-5 |
| M5 | Dashboard backend (агрегация) | 2-3 |
| M6 | Frontend Dashboard (сетки, квадратики) | 4-5 |
| M7 | Frontend таблицы (6 источников) | 5-6 |
| M8 | Frontend CRUD UI (модальные окна) | 3-4 |
| M9 | Frontend импорт (dialog, drag-drop) | 3-4 |
| M10 | Экспорт в Excel | 2 |
| M11 | Тестирование, баг-фиксинг | 4-5 |
| M12 | Документация, деплой | 2-3 |

---

## ⚡ Quick Start

```bash
# Клонировать репо
git clone <repo>
cd compliance-monitor

# Запустить через Docker Compose
docker-compose up

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# Database: postgres://localhost:5432
```

---

## ✅ Acceptance Criteria (примеры)

- ✓ Dashboard отображает % выполнения с точностью до 1%
- ✓ Сетка квадратиков перерисовывается при каждом изменении статуса
- ✓ Excel файл с 100+ строк загружается за < 5 сек
- ✓ Ошибки импорта выводятся с указанием row и field
- ✓ Inline редактирование сохраняется автоматически (debounce 500ms)
- ✓ Удаление требует подтверждения
- ✓ Все endpoints покрыты unit/integration тестами

---

## 📋 Context7 Items (нужно уточнить в docs)

- FastAPI dependency injection (`Depends()`)
- SQLAlchemy relationships & cascade delete
- Alembic auto-migration
- Pydantic v2 validators
- openpyxl reading/writing merged cells
- React `useCallback` & `useMemo` оптимизация
- Shadcn/ui Table component
- Axios interceptors
- Docker Compose networking
- PostgreSQL JSONB queries

---

## 🚨 Risks & Mitigation

| Риск | Вероятность | Решение |
|------|-----------|---------|
| Неправильная структура Excel | High | Подробные error messages, preview перед импортом |
| Дублирование при импорте | Medium | Дедупликация по (process_name, table_source) |
| Race condition при редактировании | Low | Optimistic/Pessimistic locking |
| Timeout на больших файлах | Medium | Асинхронная обработка (Celery, если нужна) |
| Потеря соединения с БД | Low | Connection pooling + retry logic |

---

## 📞 Open Questions

1. **Авторизация нужна?** (сейчас public)
2. **История версий записей?** (для отката изменений)
3. **Асинхронный импорт?** (если файлы > 50k строк)
4. **Webhook notifications?** (при завершении импорта)
5. **Multiple sheets в Excel?**
6. **Backup стратегия БД?**

---

**Статус:** ✅ Ready for Development  
**Полное ТЗ:** см. `TZ_CFT_Compliance_Monitor.md` (787 строк)
