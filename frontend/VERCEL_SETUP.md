# 🔧 Настройка Vercel для React Router

## Проблема 404 NOT_FOUND

Если вы видите ошибку 404 на Vercel, это означает, что маршруты React Router не настроены правильно.

## ✅ Решение

### 1. Проверьте настройки проекта в Vercel:

1. Зайдите в настройки проекта на Vercel
2. Перейдите в **Settings** → **General**
3. Убедитесь, что:
   - **Root Directory**: `frontend` (если проект в подпапке)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### 2. Файл vercel.json уже настроен правильно

Файл `vercel.json` содержит правильные rewrites для React Router.

### 3. Пересоберите проект

После обновления `vercel.json`:
1. Закоммитьте изменения
2. Отправьте в Git
3. Vercel автоматически пересоберет проект

### 4. Альтернативное решение (если не помогает)

Если проблема сохраняется, создайте файл `public/_redirects`:

```
/*    /index.html   200
```

Или используйте `vercel.json` с более явной конфигурацией (уже сделано).

## 🔍 Проверка

После деплоя проверьте:
- Главная страница: `https://your-project.vercel.app/`
- Страница детализации: `https://your-project.vercel.app/details`

Обе должны работать без ошибок 404.
