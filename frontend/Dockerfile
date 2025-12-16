FROM node:18-alpine

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json package-lock.json* ./
RUN npm install

# Копируем код
COPY . .

# Команда запуска
CMD ["npm", "run", "dev", "--", "--host"]

