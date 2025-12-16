# 🚀 Пошаговая инструкция: Деплой Backend на Railway

## 📋 Что нужно сделать

1. Создать аккаунт на Railway
2. Подключить GitHub репозиторий
3. Настроить PostgreSQL базу данных
4. Настроить переменные окружения
5. Применить миграции
6. Получить URL backend
7. Настроить переменную в Vercel

---

## Шаг 1: Создание аккаунта на Railway

1. Перейдите на https://railway.app
2. Нажмите **"Start a New Project"** или **"Login"**
3. Войдите через **GitHub** (используйте тот же аккаунт, что и для Vercel)

---

## Шаг 2: Создание проекта из GitHub

1. После входа нажмите **"+ New Project"**
2. Выберите **"Deploy from GitHub repo"**
3. Найдите и выберите репозиторий: **`infoscraper/check-lists-overview`**
4. Railway начнет сканировать репозиторий

---

## Шаг 3: Настройка Root Directory

После подключения репозитория:

1. Railway покажет список сервисов
2. Нажмите на созданный сервис (обычно называется по имени репозитория)
3. Перейдите в **"Settings"** (вкладка сверху)
4. Найдите раздел **"Root Directory"**
5. Укажите: **`backend`**
6. Нажмите **"Save"**

Railway автоматически определит Dockerfile и начнет сборку.

---

## Шаг 4: Добавление PostgreSQL базы данных

1. В вашем проекте Railway нажмите **"+ New"**
2. Выберите **"Database"** → **"Add PostgreSQL"**
3. Railway автоматически создаст базу данных
4. **Важно:** Railway автоматически создаст переменную `DATABASE_URL` - ничего делать не нужно!

---

## Шаг 5: Настройка переменных окружения

1. Вернитесь к вашему сервису (backend)
2. Перейдите в **"Variables"** (вкладка сверху)
3. Нажмите **"+ New Variable"**

Добавьте следующие переменные:

### Обязательные переменные:

1. **ENVIRONMENT**
   - Value: `production`
   - Description: Окружение приложения

2. **SECRET_KEY**
   - Value: Сгенерируйте случайный ключ (можно использовать: `openssl rand -hex 32` или любой случайный набор символов)
   - Пример: `your-super-secret-key-change-this-in-production-12345`
   - Description: Секретный ключ для приложения

3. **LOG_LEVEL**
   - Value: `INFO`
   - Description: Уровень логирования

4. **CORS_ORIGINS**
   - Value: `["https://check-lists-cft.vercel.app", "https://check-lists-cft-infoscrapers-projects.vercel.app"]`
   - Description: Разрешенные домены для CORS

### Автоматические переменные (Railway создаст сам):

- `DATABASE_URL` - создается автоматически при добавлении PostgreSQL
- `PORT` - устанавливается автоматически Railway

---

## Шаг 6: Применение миграций базы данных

После того, как Railway задеплоит backend:

1. В Railway откройте ваш сервис (backend)
2. Перейдите во вкладку **"Deployments"**
3. Найдите последний успешный деплоймент
4. Нажмите на три точки (⋯) → **"Open Shell"** или найдите кнопку **"Shell"**
5. В открывшемся терминале выполните:
   ```bash
   alembic upgrade head
   ```

Или используйте Railway CLI:
```bash
railway login
railway link
railway run alembic upgrade head
```

---

## Шаг 7: Получение URL вашего backend

1. В Railway откройте ваш сервис (backend)
2. Перейдите во вкладку **"Settings"**
3. Найдите раздел **"Networking"** или **"Domains"**
4. Скопируйте **Public Domain** (будет что-то вроде: `your-project.up.railway.app`)
5. Это и есть URL вашего backend!

Или посмотрите во вкладку **"Deployments"** - там будет показан URL.

---

## Шаг 8: Настройка переменной в Vercel

Теперь нужно указать этот URL в Vercel:

1. Откройте проект в Vercel: https://vercel.com/infoscrapers-projects/check-lists-cft
2. Перейдите в **Settings** → **Environment Variables**
3. Нажмите **"+ Add New"**
4. Заполните:
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** URL вашего Railway backend (например, `https://your-project.up.railway.app`)
   - **Environment:** Отметьте все три:
     - ✅ Production
     - ✅ Preview
     - ✅ Development
5. Нажмите **"Save"**
6. Vercel автоматически начнет новый деплоймент

---

## ✅ Проверка работы

После завершения всех шагов:

1. **Проверьте backend:**
   - Откройте `https://your-backend-url.up.railway.app/health`
   - Должен вернуться: `{"status":"ok"}`
   - Откройте `https://your-backend-url.up.railway.app/docs`
   - Должна открыться Swagger документация API

2. **Проверьте frontend:**
   - Откройте https://check-lists-cft.vercel.app
   - Попробуйте добавить чек-лист
   - Ошибка "Network Error" должна исчезнуть

---

## 🆘 Решение проблем

### Проблема: Railway не находит Dockerfile

**Решение:**
- Убедитесь, что Root Directory установлен в `backend`
- Проверьте, что файл `backend/Dockerfile` существует в репозитории

### Проблема: Ошибка подключения к базе данных

**Решение:**
- Проверьте, что PostgreSQL добавлен в проект
- Убедитесь, что переменная `DATABASE_URL` создана автоматически
- Проверьте логи в Railway (вкладка "Deployments" → выберите деплоймент → "View Logs")

### Проблема: CORS ошибки

**Решение:**
- Убедитесь, что в `CORS_ORIGINS` указаны правильные URL Vercel
- Формат должен быть JSON массив: `["https://check-lists-cft.vercel.app"]`
- После изменения переменной перезапустите сервис в Railway

### Проблема: Миграции не применяются

**Решение:**
- Убедитесь, что файлы миграций есть в папке `backend/migrations`
- Проверьте, что `alembic.ini` находится в папке `backend`
- Выполните команду из корня проекта: `railway run --service backend alembic upgrade head`

---

## 📝 Полезные команды Railway CLI

Если установите Railway CLI:

```bash
# Установка Railway CLI
npm i -g @railway/cli

# Вход в Railway
railway login

# Подключение к проекту
railway link

# Просмотр логов
railway logs

# Выполнение команд в контейнере
railway run alembic upgrade head

# Просмотр переменных окружения
railway variables
```

---

## 💰 Стоимость

- **Railway Free Tier:** $5 бесплатных кредитов в месяц (обычно хватает для небольших проектов)
- **Railway Pro:** $5/месяц (если нужны дополнительные ресурсы)

Для начала Free Tier должно хватить!

---

## 🎉 Готово!

После выполнения всех шагов у вас будет:
- ✅ Backend на Railway с PostgreSQL
- ✅ Frontend на Vercel
- ✅ Все настроено и работает

Если возникнут проблемы - проверьте логи в Railway и Vercel, они помогут найти причину.
