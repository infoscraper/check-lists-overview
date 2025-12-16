# 🚀 Быстрый старт - Compliance Progress Monitor

## ✅ Что уже настроено

Все конфигурации уже настроены с **дефолтными значениями**, которые работают "из коробки":

- ✅ **Docker Compose** - использует дефолтные значения для всех переменных
- ✅ **Backend** - имеет дефолтные значения в коде
- ✅ **Frontend** - настроен на `http://localhost:8000` для API
- ✅ **База данных** - пароль по умолчанию: `compliance123`

## 🎯 Запуск без дополнительных настроек

Просто выполните:

```bash
# 1. Перейти в папку проекта
cd "Чек-листы/check_lists_overview"

# 2. Запустить все сервисы
docker-compose up -d

# 3. Применить миграции БД (первый раз)
docker-compose exec backend alembic upgrade head

# 4. Открыть в браузере
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# Swagger:   http://localhost:8000/docs
```

**Всё!** Приложение должно работать без дополнительных настроек.

---

## ⚙️ Опционально: Настройка переменных окружения

Если хотите изменить дефолтные значения, создайте файл `.env` в корне проекта:

```bash
# .env (в корне проекта)
DB_PASSWORD=ваш_пароль
ENVIRONMENT=production
SECRET_KEY=ваш-секретный-ключ
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://your-domain.com"]
```

Или создайте `backend/.env` для более детальной настройки backend:

```bash
# backend/.env
DATABASE_URL=postgresql://compliance:ваш_пароль@postgres:5432/compliance_db
SECRET_KEY=ваш-секретный-ключ
LOG_LEVEL=INFO
```

**Примечание:** Если не создадите `.env` файлы, всё будет работать с дефолтными значениями.

---

## 🔍 Проверка работы

После запуска проверьте:

1. **Статус контейнеров:**
   ```bash
   docker-compose ps
   ```
   Все должны быть в статусе "Up"

2. **Логи backend:**
   ```bash
   docker-compose logs backend
   ```
   Должны быть сообщения о запуске сервера

3. **Логи frontend:**
   ```bash
   docker-compose logs frontend
   ```
   Должен быть запущен Vite dev server

4. **Проверка API:**
   ```bash
   curl http://localhost:8000/health
   ```
   Должен вернуть `{"status":"ok"}`

---

## 🐛 Решение проблем

### Проблема: Контейнеры не запускаются

**Решение:**
```bash
# Проверить логи
docker-compose logs

# Пересобрать контейнеры
docker-compose up -d --build
```

### Проблема: База данных не подключается

**Решение:**
```bash
# Проверить, что PostgreSQL запущен
docker-compose ps postgres

# Проверить подключение
docker-compose exec postgres psql -U compliance -d compliance_db -c "SELECT 1;"
```

### Проблема: Frontend не видит API

**Решение:**
- Убедитесь, что backend запущен на порту 8000
- Проверьте переменную `VITE_API_BASE_URL` в docker-compose.yml
- Проверьте CORS настройки в backend

---

## 📝 Дефолтные значения (если не указаны)

| Переменная | Дефолтное значение |
|------------|---------------------|
| `DB_PASSWORD` | `compliance123` |
| `DATABASE_URL` | `postgresql://compliance:compliance123@postgres:5432/compliance_db` |
| `ENVIRONMENT` | `development` |
| `SECRET_KEY` | `your-secret-key-change-in-production` |
| `LOG_LEVEL` | `INFO` |
| `CORS_ORIGINS` | `["http://localhost:3000"]` |
| `VITE_API_BASE_URL` | `http://localhost:8000` |

---

## 🎉 Готово!

После выполнения команд выше приложение будет доступно:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

Никаких дополнительных настроек не требуется! 🚀

