# 🔧 Настройка переменных окружения в Vercel

## Проблема: Network Error

Если вы видите ошибку "Network Error" в развернутом приложении, это означает, что переменная окружения `VITE_API_BASE_URL` не установлена в Vercel.

## ✅ Решение: Пошаговая инструкция

### Шаг 1: Убедитесь, что backend задеплоен

Backend должен быть доступен по публичному URL. Если еще не задеплоен:

1. **Railway** (рекомендуется):
   - Зайдите на https://railway.app
   - Создайте новый проект из GitHub репозитория
   - Выберите папку `backend`
   - Добавьте PostgreSQL базу данных
   - Railway автоматически создаст URL вида: `https://your-project.railway.app`

2. **Render** (альтернатива):
   - Зайдите на https://render.com
   - Создайте новый Web Service из GitHub репозитория
   - Выберите папку `backend`
   - Добавьте PostgreSQL базу данных
   - Render создаст URL вида: `https://your-project.onrender.com`

### Шаг 2: Настройте переменные окружения в Vercel

1. **Откройте проект в Vercel:**
   - Перейдите на https://vercel.com/infoscrapers-projects/check-lists-cft
   - Или откройте ваш проект в Vercel Dashboard

2. **Перейдите в настройки переменных окружения:**
   - Нажмите на вкладку **"Settings"** (вверху)
   - В левом меню выберите **"Environment Variables"**

3. **Добавьте переменную:**
   - Нажмите **"+ Add New"**
   - **Key (Имя):** `VITE_API_BASE_URL`
   - **Value (Значение):** URL вашего backend (например, `https://your-backend.railway.app`)
   - **Environment (Окружение):** Отметьте все три:
     - ✅ Production
     - ✅ Preview  
     - ✅ Development
   - Нажмите **"Save"**

4. **Пересоберите проект:**
   - После сохранения переменной Vercel автоматически начнет новый деплоймент
   - Или перейдите в **"Deployments"** и нажмите **"Redeploy"** на последнем деплойменте

### Шаг 3: Проверьте настройки CORS на backend

Убедитесь, что в backend настроен CORS для домена Vercel:

```env
CORS_ORIGINS=["https://check-lists-cft.vercel.app", "https://check-lists-cft-infoscrapers-projects.vercel.app"]
```

### Шаг 4: Проверьте работу

После пересборки:
1. Откройте https://check-lists-cft.vercel.app
2. Попробуйте добавить чек-лист
3. Ошибка "Network Error" должна исчезнуть

## 🔍 Проверка текущих переменных окружения

Чтобы проверить, какие переменные установлены:
1. Откройте проект в Vercel
2. Settings → Environment Variables
3. Вы увидите список всех переменных

## ⚠️ Важно

- Переменные с префиксом `VITE_` доступны в браузере
- После изменения переменных нужно пересобрать проект
- Убедитесь, что backend доступен и отвечает на запросы

## 🆘 Если проблема сохраняется

1. Проверьте логи в Vercel (вкладка "Logs")
2. Проверьте логи backend
3. Убедитесь, что URL backend правильный и доступен
4. Проверьте CORS настройки на backend
