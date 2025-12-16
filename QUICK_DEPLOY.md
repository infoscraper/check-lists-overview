# ⚡ Быстрый деплой на Vercel + Railway

## 🎯 Что нужно сделать

### 1. Frontend → Vercel (5 минут)

1. Зайдите на [vercel.com](https://vercel.com) и войдите через GitHub
2. Нажмите "Add New Project"
3. Выберите ваш репозиторий
4. Настройки:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Добавьте переменную окружения:
   - `VITE_API_BASE_URL` = `https://your-backend.railway.app` (заполните после деплоя backend)
6. Нажмите "Deploy"

### 2. Backend + PostgreSQL → Railway (10 минут)

1. Зайдите на [railway.app](https://railway.app) и войдите через GitHub
2. Нажмите "New Project" → "Deploy from GitHub"
3. Выберите ваш репозиторий
4. Railway автоматически определит `backend/Dockerfile`
5. Добавьте PostgreSQL:
   - Нажмите "+ New" → "Database" → "PostgreSQL"
   - Railway создаст переменную `DATABASE_URL` автоматически
6. Настройте переменные окружения:
   ```
   ENVIRONMENT=production
   SECRET_KEY=<сгенерируйте случайный ключ>
   LOG_LEVEL=INFO
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```
7. Railway автоматически задеплоит backend
8. Примените миграции:
   - Откройте терминал в Railway
   - Выполните: `alembic upgrade head`

### 3. Обновите переменные

1. **В Vercel**: Обновите `VITE_API_BASE_URL` на URL вашего Railway backend
2. **В Railway**: Обновите `CORS_ORIGINS` на URL вашего Vercel frontend
3. Перезапустите оба сервиса

## ✅ Готово!

Теперь ваш проект доступен:
- Frontend: `https://your-project.vercel.app`
- Backend: `https://your-project.railway.app`
- API Docs: `https://your-project.railway.app/docs`

## 📝 Важные моменты

- **CORS**: Убедитесь, что URL в `CORS_ORIGINS` точно совпадает с URL Vercel (включая https://)
- **Переменные**: Все переменные с `VITE_` префиксом доступны в frontend
- **Миграции**: Не забудьте применить миграции после первого деплоя
- **Логи**: Используйте логи в Railway и Vercel для отладки

## 🆘 Проблемы?

Смотрите подробную инструкцию в `DEPLOY.md`
