# Compliance Progress Monitor

Веб-приложение для мониторинга прогресса процессов тестирования в ЦФТ-Банк.

## 🚀 Быстрый старт

### Требования
- Docker и Docker Compose
- Git

### Запуск

```bash
# 1. Клонировать репозиторий (если нужно)
cd "Чек-листы/check_lists_overview"

# 2. Запустить все сервисы через Docker Compose
docker-compose up -d

# 3. Применить миграции БД (первый запуск)
# Найдите имя контейнера: docker ps
# Затем выполните:
docker exec <backend-container-name> alembic upgrade head
# Или используйте docker-compose:
docker-compose exec backend alembic upgrade head

# 4. Открыть в браузере
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# Swagger:   http://localhost:8000/docs
```

## 📁 Структура проекта

```
check_lists_overview/
├── backend/              # Python/FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── db/          # Database configuration
│   ├── migrations/      # Alembic migrations
│   └── requirements.txt
├── frontend/            # React/TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── api/         # API client
│   │   └── types/       # TypeScript types
│   └── package.json
└── docker-compose.yml
```

## 🔧 Разработка

### Backend

```bash
# Войти в контейнер
docker-compose exec backend bash
# или
docker exec -it <backend-container-name> bash

# Создать миграцию
alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

### Frontend

```bash
# Войти в контейнер
docker-compose exec frontend sh
# или
docker exec -it <frontend-container-name> sh

# Установить зависимости (если нужно)
npm install

# Запуск уже работает через docker-compose
```

## 📊 Основные функции

1. **Dashboard** - обзор прогресса с визуализацией
2. **Детализация** - таблицы для каждого источника данных
3. **Импорт Excel** - загрузка данных из Excel файлов
4. **CRUD операции** - создание, редактирование, удаление записей
5. **Экспорт Excel** - выгрузка данных в Excel

## 🔌 API Endpoints

- `GET /api/dashboard/summary` - сводка для dashboard
- `GET /api/records` - список записей (с фильтрацией)
- `POST /api/records` - создать запись
- `PUT /api/records/{id}` - обновить запись
- `DELETE /api/records/{id}` - удалить запись
- `POST /api/import/excel` - импорт Excel
- `GET /api/export/excel` - экспорт Excel

Полная документация API доступна на `/docs` (Swagger UI).

## 🗄️ База данных

PostgreSQL 15 с таблицами:
- `process_records` - основные записи процессов
- `import_logs` - логи импортов

## 📝 Переменные окружения

Создайте файл `backend/.env` на основе `backend/.env.example`:

```env
ENVIRONMENT=development
DATABASE_URL=postgresql://compliance:compliance123@postgres:5432/compliance_db
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:3000"]
```

## 🐳 Docker команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Логи
docker-compose logs -f backend
docker-compose logs -f frontend

# Пересборка
docker-compose up -d --build

# Очистка данных
docker-compose down -v
```

## 📚 Документация

- Полное ТЗ: `TZ_CFT_Compliance_Monitor.md`
- Краткий обзор: `SUMMARY_CFT_Compliance.md`
- Справочник маппинга: `MAPPING_REFERENCE.md`
- Шпаргалка: `QUICK_REFERENCE.md`

## ✅ Статус

- ✅ Backend API (FastAPI)
- ✅ Frontend (React + TypeScript)
- ✅ Импорт Excel
- ✅ Экспорт Excel
- ✅ Dashboard
- ✅ CRUD операции
- ✅ Docker Compose

## 🐛 Известные проблемы

- При первом запуске может потребоваться подождать несколько секунд для инициализации БД
- Для больших файлов Excel (>10k строк) может потребоваться увеличение timeout

## 📞 Поддержка

При возникновении проблем проверьте:
1. Логи контейнеров: `docker-compose logs`
2. Статус контейнеров: `docker-compose ps`
3. Подключение к БД: `docker-compose exec postgres psql -U compliance -d compliance_db`

