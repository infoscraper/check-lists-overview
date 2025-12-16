# 🖥️ Деплой Backend на собственный VPS сервер

## 📋 Информация о вашем сервере

- **IP:** 31.97.79.59
- **Hostname:** srv1066622.hstgr.cloud
- **OS:** Ubuntu (KVM)
- **Статус:** Running

---

## 🎯 План деплоя

1. Подключение к серверу
2. Установка необходимого ПО (Docker или Python)
3. Установка PostgreSQL
4. Настройка Nginx (reverse proxy)
5. Деплой приложения
6. Настройка SSL (Let's Encrypt)
7. Настройка автозапуска

---

## Шаг 1: Подключение к серверу

```bash
ssh root@31.97.79.59
# или
ssh root@srv1066622.hstgr.cloud
```

Если используете ключ SSH:
```bash
ssh -i /path/to/your/key root@31.97.79.59
```

---

## Шаг 2: Обновление системы

```bash
apt update && apt upgrade -y
```

---

## Шаг 3: Установка необходимого ПО

### Вариант A: Использование Docker (Рекомендуется)

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
apt install docker-compose -y

# Проверка установки
docker --version
docker-compose --version
```

### Вариант B: Прямая установка Python

```bash
# Установка Python 3.11 и зависимостей
apt install python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx git -y
```

---

## Шаг 4: Установка PostgreSQL

### Если используете Docker:

Создайте файл `docker-compose.yml`:

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    container_name: compliance_postgres
    environment:
      POSTGRES_USER: compliance
      POSTGRES_PASSWORD: ваш_надежный_пароль
      POSTGRES_DB: compliance_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "127.0.0.1:5432:5432"  # Только локальный доступ
    restart: unless-stopped

volumes:
  postgres_data:
```

Запустите:
```bash
docker-compose up -d
```

### Если используете прямую установку:

```bash
# PostgreSQL уже установлен, настройте его
sudo -u postgres psql

# В psql выполните:
CREATE USER compliance WITH PASSWORD 'ваш_надежный_пароль';
CREATE DATABASE compliance_db OWNER compliance;
GRANT ALL PRIVILEGES ON DATABASE compliance_db TO compliance;
\q
```

---

## Шаг 5: Клонирование репозитория

```bash
# Создайте директорию для проекта
mkdir -p /opt/compliance-monitor
cd /opt/compliance-monitor

# Клонируйте репозиторий
git clone https://github.com/infoscraper/check-lists-overview.git .

# Перейдите в папку backend
cd backend
```

---

## Шаг 6: Настройка приложения

### Если используете Docker:

Создайте файл `.env` в папке `backend`:

```env
DATABASE_URL=postgresql://compliance:ваш_пароль@postgres:5432/compliance_db
ENVIRONMENT=production
SECRET_KEY=ваш-секретный-ключ-минимум-32-символа
LOG_LEVEL=INFO
CORS_ORIGINS=["https://check-lists-cft.vercel.app"]
PORT=8000
```

Обновите `docker-compose.yml`:

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    container_name: compliance_postgres
    environment:
      POSTGRES_USER: compliance
      POSTGRES_PASSWORD: ваш_надежный_пароль
      POSTGRES_DB: compliance_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "127.0.0.1:5432:5432"
    restart: unless-stopped
    networks:
      - compliance_network

  backend:
    build: ./backend
    container_name: compliance_backend
    environment:
      DATABASE_URL: postgresql://compliance:ваш_пароль@postgres:5432/compliance_db
      ENVIRONMENT: production
      SECRET_KEY: ваш-секретный-ключ
      LOG_LEVEL: INFO
      CORS_ORIGINS: '["https://check-lists-cft.vercel.app"]'
      PORT: 8000
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      - postgres
    restart: unless-stopped
    networks:
      - compliance_network
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

volumes:
  postgres_data:

networks:
  compliance_network:
```

Запустите:
```bash
docker-compose up -d --build
```

### Если используете прямую установку:

```bash
cd /opt/compliance-monitor/backend

# Создайте виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте файл .env
cat > .env << EOF
DATABASE_URL=postgresql://compliance:ваш_пароль@localhost:5432/compliance_db
ENVIRONMENT=production
SECRET_KEY=ваш-секретный-ключ-минимум-32-символа
LOG_LEVEL=INFO
CORS_ORIGINS=["https://check-lists-cft.vercel.app"]
EOF
```

---

## Шаг 7: Применение миграций

### Docker:
```bash
docker-compose exec backend alembic upgrade head
```

### Прямая установка:
```bash
cd /opt/compliance-monitor/backend
source venv/bin/activate
alembic upgrade head
```

---

## Шаг 8: Настройка Nginx (Reverse Proxy)

Создайте конфигурацию Nginx:

```bash
nano /etc/nginx/sites-available/compliance-backend
```

Вставьте следующее:

```nginx
server {
    listen 80;
    server_name 31.97.79.59 srv1066622.hstgr.cloud;

    # Логи
    access_log /var/log/nginx/compliance-backend-access.log;
    error_log /var/log/nginx/compliance-backend-error.log;

    # Проксирование на backend
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Таймауты для больших файлов (импорт Excel)
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Увеличение размера загружаемых файлов
    client_max_body_size 50M;
}
```

Активируйте конфигурацию:

```bash
ln -s /etc/nginx/sites-available/compliance-backend /etc/nginx/sites-enabled/
nginx -t  # Проверка конфигурации
systemctl restart nginx
```

---

## Шаг 9: Настройка SSL (Let's Encrypt)

```bash
# Установка Certbot
apt install certbot python3-certbot-nginx -y

# Получение сертификата (если есть домен)
certbot --nginx -d ваш-домен.com

# Или для IP адреса (без домена) - используйте самоподписанный сертификат
# или пропустите этот шаг, если используете только IP
```

**Важно:** Если у вас нет домена, можно использовать IP адрес, но HTTPS будет с предупреждением. Для продакшена лучше использовать домен.

---

## Шаг 10: Настройка автозапуска

### Если используете Docker:

Docker Compose уже настроен на автозапуск (`restart: unless-stopped`).

### Если используете прямую установку:

Создайте systemd сервис:

```bash
nano /etc/systemd/system/compliance-backend.service
```

Вставьте:

```ini
[Unit]
Description=Compliance Monitor Backend
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/compliance-monitor/backend
Environment="PATH=/opt/compliance-monitor/backend/venv/bin"
ExecStart=/opt/compliance-monitor/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:

```bash
systemctl daemon-reload
systemctl enable compliance-backend
systemctl start compliance-backend
systemctl status compliance-backend
```

---

## Шаг 11: Настройка Firewall

```bash
# Установка UFW (если не установлен)
apt install ufw -y

# Разрешить SSH
ufw allow 22/tcp

# Разрешить HTTP и HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Включить firewall
ufw enable

# Проверка статуса
ufw status
```

---

## Шаг 12: Проверка работы

1. **Проверьте backend:**
   ```bash
   curl http://localhost:8000/health
   # Должно вернуть: {"status":"ok"}
   ```

2. **Проверьте через Nginx:**
   ```bash
   curl http://31.97.79.59/health
   # Должно вернуть: {"status":"ok"}
   ```

3. **Проверьте Swagger:**
   - Откройте в браузере: `http://31.97.79.59/docs`

---

## Шаг 13: Настройка Vercel

Теперь в Vercel установите переменную окружения:

1. Vercel → ваш проект → **Settings** → **Environment Variables**
2. Добавьте: `VITE_API_BASE_URL` = `http://31.97.79.59` (или `https://` если настроили SSL)
3. Vercel автоматически пересоберет проект

---

## 🔄 Обновление приложения

### Docker:
```bash
cd /opt/compliance-monitor
git pull
cd backend
docker-compose up -d --build
docker-compose exec backend alembic upgrade head
```

### Прямая установка:
```bash
cd /opt/compliance-monitor
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
systemctl restart compliance-backend
```

---

## 📊 Мониторинг и логи

### Docker:
```bash
# Логи backend
docker-compose logs -f backend

# Логи PostgreSQL
docker-compose logs -f postgres

# Статус контейнеров
docker-compose ps
```

### Прямая установка:
```bash
# Логи backend
journalctl -u compliance-backend -f

# Логи Nginx
tail -f /var/log/nginx/compliance-backend-access.log
tail -f /var/log/nginx/compliance-backend-error.log

# Логи PostgreSQL
tail -f /var/log/postgresql/postgresql-*.log
```

---

## 🆘 Решение проблем

### Проблема: Backend не запускается

**Решение:**
```bash
# Проверьте логи
docker-compose logs backend
# или
journalctl -u compliance-backend -n 50

# Проверьте подключение к БД
docker-compose exec backend python -c "from app.db.database import engine; engine.connect()"
```

### Проблема: Nginx возвращает 502

**Решение:**
- Проверьте, что backend запущен: `curl http://localhost:8000/health`
- Проверьте конфигурацию Nginx: `nginx -t`
- Проверьте логи Nginx: `tail -f /var/log/nginx/compliance-backend-error.log`

### Проблема: CORS ошибки

**Решение:**
- Убедитесь, что в `.env` правильно указан `CORS_ORIGINS`
- Перезапустите backend после изменения переменных

---

## 🔒 Безопасность

1. **Измените пароли по умолчанию**
2. **Настройте SSH ключи** вместо паролей
3. **Регулярно обновляйте систему:** `apt update && apt upgrade`
4. **Настройте fail2ban** для защиты от брутфорса:
   ```bash
   apt install fail2ban -y
   systemctl enable fail2ban
   systemctl start fail2ban
   ```
5. **Используйте домен** вместо IP для SSL сертификата

---

## ✅ Готово!

После выполнения всех шагов:
- ✅ Backend доступен на `http://31.97.79.59` (или `https://` с SSL)
- ✅ PostgreSQL настроен и работает
- ✅ Nginx проксирует запросы
- ✅ Приложение автозапускается при перезагрузке сервера

---

## 📝 Полезные команды

```bash
# Перезапуск backend (Docker)
docker-compose restart backend

# Перезапуск backend (Systemd)
systemctl restart compliance-backend

# Перезапуск Nginx
systemctl restart nginx

# Проверка статуса
systemctl status compliance-backend
docker-compose ps

# Просмотр логов в реальном времени
docker-compose logs -f
journalctl -u compliance-backend -f
```
