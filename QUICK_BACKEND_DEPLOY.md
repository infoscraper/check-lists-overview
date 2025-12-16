# ⚡ Быстрый деплой Backend на Railway (5 минут)

## 🎯 Быстрые шаги

### 1. Railway (2 минуты)
1. Зайдите на https://railway.app → Login через GitHub
2. **"+ New Project"** → **"Deploy from GitHub repo"**
3. Выберите: **`infoscraper/check-lists-overview`**
4. В настройках сервиса укажите **Root Directory: `backend`**
5. Railway автоматически найдет Dockerfile и начнет сборку

### 2. PostgreSQL (1 минута)
1. В проекте Railway: **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Готово! `DATABASE_URL` создастся автоматически

### 3. Переменные окружения (1 минута)
В настройках backend сервиса → **"Variables"** → **"+ New Variable"**:

```
ENVIRONMENT=production
SECRET_KEY=ваш-случайный-ключ-здесь-минимум-32-символа
LOG_LEVEL=INFO
CORS_ORIGINS=["https://check-lists-cft.vercel.app"]
```

### 4. Получить URL (30 секунд)
1. В Railway: ваш сервис → **"Settings"** → **"Networking"**
2. Скопируйте **Public Domain** (например: `your-project.up.railway.app`)

### 5. Настроить Vercel (1 минута)
1. Vercel → ваш проект → **Settings** → **Environment Variables**
2. Добавьте: `VITE_API_BASE_URL` = URL из шага 4
3. Vercel автоматически пересоберет проект

## ✅ Готово!

Откройте https://check-lists-cft.vercel.app и проверьте работу.

---

## 📝 Примечания

- **Миграции:** После первого деплоя выполните `railway run alembic upgrade head` (или создайте миграции локально и закоммитьте)
- **Логи:** Смотрите в Railway → ваш сервис → **"Deployments"** → выберите деплоймент → **"View Logs"**
- **Проблемы:** Проверьте, что Root Directory = `backend` и все переменные установлены

Подробная инструкция: см. `BACKEND_DEPLOY_GUIDE.md`
