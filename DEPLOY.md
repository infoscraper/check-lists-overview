# 🚀 Инструкция по деплою

## Архитектура деплоя

- **Frontend** → Vercel (React + Vite)
- **Backend** → Railway/Render (FastAPI + Docker)
- **PostgreSQL** → Supabase/Neon (бесплатные) или Railway

---

## 📦 Вариант 1: Vercel + Railway (Рекомендуется)

### 1. Frontend на Vercel

#### Шаги:
1. **Подготовка:**
   ```bash
   cd frontend
   ```

2. **Создайте файл `.env.production`** (опционально, можно настроить в Vercel):
   ```env
   VITE_API_BASE_URL=https://your-backend-url.railway.app
   ```

3. **Деплой через Vercel CLI:**
   ```bash
   npm i -g vercel
   vercel login
   vercel --prod
   ```

4. **Или через GitHub:**
   - Подключите репозиторий к Vercel
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variables:
     - `VITE_API_BASE_URL` = `https://your-backend-url.railway.app`

### 2. Backend на Railway

#### Шаги:
1. **Создайте аккаунт на [Railway](https://railway.app)**

2. **Создайте новый проект:**
   - New Project → Deploy from GitHub
   - Выберите репозиторий
   - Root Directory: `backend`

3. **Добавьте PostgreSQL:**
   - New → Database → PostgreSQL
   - Railway автоматически создаст переменную `DATABASE_URL`

4. **Настройте переменные окружения:**
   ```
   DATABASE_URL=<автоматически из PostgreSQL>
   ENVIRONMENT=production
   SECRET_KEY=<сгенерируйте случайный ключ>
   LOG_LEVEL=INFO
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```

5. **Railway автоматически определит Dockerfile и задеплоит**

6. **Примените миграции:**
   ```bash
   railway run alembic upgrade head
   ```

### 3. Обновите CORS в backend

После деплоя frontend, обновите `CORS_ORIGINS` в Railway:
```
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

---

## 📦 Вариант 2: Vercel + Render

### 1. Frontend на Vercel
(Аналогично варианту 1)

### 2. Backend на Render

#### Шаги:
1. **Создайте аккаунт на [Render](https://render.com)**

2. **Создайте PostgreSQL:**
   - New → PostgreSQL
   - Запишите `Internal Database URL`

3. **Создайте Web Service:**
   - New → Web Service
   - Connect GitHub репозиторий
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     ```
     DATABASE_URL=<из PostgreSQL>
     ENVIRONMENT=production
     SECRET_KEY=<сгенерируйте>
     LOG_LEVEL=INFO
     CORS_ORIGINS=["https://your-frontend.vercel.app"]
     PORT=10000
     ```

4. **Примените миграции:**
   ```bash
   render run alembic upgrade head
   ```

---

## 📦 Вариант 3: PostgreSQL на Supabase/Neon

Если хотите использовать внешнюю БД:

### Supabase:
1. Создайте проект на [Supabase](https://supabase.com)
2. Получите Connection String из Settings → Database
3. Используйте его как `DATABASE_URL` в Railway/Render

### Neon:
1. Создайте проект на [Neon](https://neon.tech)
2. Получите Connection String
3. Используйте его как `DATABASE_URL` в Railway/Render

---

## 🔧 Настройка переменных окружения

### Frontend (Vercel):
```
VITE_API_BASE_URL=https://your-backend-url.railway.app
```

### Backend (Railway/Render):
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

---

## ✅ Чек-лист после деплоя

- [ ] Frontend доступен на Vercel
- [ ] Backend доступен и отвечает на `/health`
- [ ] CORS настроен правильно
- [ ] Миграции применены (`alembic upgrade head`)
- [ ] Переменные окружения настроены
- [ ] Frontend может обращаться к Backend API
- [ ] Импорт Excel работает
- [ ] Dashboard отображается корректно

---

## 🐛 Решение проблем

### CORS ошибки:
- Проверьте `CORS_ORIGINS` в backend
- Убедитесь, что URL frontend указан правильно (с https://)

### Database connection:
- Проверьте `DATABASE_URL`
- Убедитесь, что БД доступна из интернета (для Supabase/Neon)
- Для Railway PostgreSQL используйте Internal Database URL

### Frontend не видит API:
- Проверьте `VITE_API_BASE_URL` в Vercel
- Убедитесь, что переменная начинается с `VITE_`
- Пересоберите проект после изменения переменных

---

## 📝 Полезные команды

### Railway:
```bash
railway login
railway link
railway logs
railway run alembic upgrade head
```

### Render:
```bash
render logs
render run alembic upgrade head
```

### Vercel:
```bash
vercel logs
vercel env pull
```

---

## 💰 Примерная стоимость

- **Vercel**: Бесплатно (Hobby plan)
- **Railway**: $5/месяц (Pro plan) или бесплатно с ограничениями
- **Render**: Бесплатно (Free tier) с ограничениями
- **Supabase**: Бесплатно до 500MB БД
- **Neon**: Бесплатно до 3GB БД

---

**Готово! 🎉**
