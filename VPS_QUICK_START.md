# ⚡ Быстрый деплой на VPS (10 минут)

## 🎯 Минимальные шаги

### 1. Подключение (1 минута)
```bash
ssh root@31.97.79.59
```

### 2. Установка Docker (2 минуты)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
apt install docker-compose -y
```

### 3. Клонирование проекта (1 минута)
```bash
mkdir -p /opt/compliance-monitor && cd /opt/compliance-monitor
git clone https://github.com/infoscraper/check-lists-overview.git .
```

### 4. Настройка переменных (1 минута)
```bash
cd /opt/compliance-monitor
nano docker-compose.production.yml
# Измените пароли и SECRET_KEY
```

### 5. Запуск (1 минута)
```bash
cd /opt/compliance-monitor
docker-compose -f docker-compose.production.yml up -d --build
docker-compose -f docker-compose.production.yml exec backend alembic upgrade head
```

### 6. Настройка Nginx (2 минуты)
```bash
# Скопируйте конфигурацию
cp nginx.conf.example /etc/nginx/sites-available/compliance-backend
ln -s /etc/nginx/sites-available/compliance-backend /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx
```

### 7. Firewall (1 минута)
```bash
ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp && ufw enable
```

### 8. Проверка (30 секунд)
```bash
curl http://31.97.79.59/health
# Должно вернуть: {"status":"ok"}
```

### 9. Настройка Vercel (1 минута)
- Vercel → Settings → Environment Variables
- Добавьте: `VITE_API_BASE_URL` = `http://31.97.79.59`

## ✅ Готово!

Подробная инструкция: см. `VPS_DEPLOY_GUIDE.md`
