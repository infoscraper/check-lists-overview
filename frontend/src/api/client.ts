import axios from 'axios';

// Получаем URL API из переменных окружения
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Проверяем, что в продакшене установлена переменная окружения
if (import.meta.env.PROD && !import.meta.env.VITE_API_BASE_URL) {
  console.error(
    '⚠️ VITE_API_BASE_URL не установлена! ' +
    'Установите переменную окружения в настройках Vercel проекта.'
  );
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 секунд таймаут
});

// Interceptors для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Сервер вернул ошибку
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Запрос был отправлен, но ответа не получено
      console.error('Network Error:', {
        message: 'Не удалось подключиться к серверу',
        url: API_BASE_URL,
        error: error.message,
        hint: import.meta.env.PROD 
          ? 'Проверьте, что VITE_API_BASE_URL установлена в Vercel и backend доступен'
          : 'Проверьте, что backend запущен на ' + API_BASE_URL
      });
    } else {
      // Что-то пошло не так при настройке запроса
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;

