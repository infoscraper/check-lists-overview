# 📋 Техническая Спецификация: Compliance Progress Monitor

Полный набор документов для разработки веб-приложения "Система мониторинга прогресса процессов" для ЦФТ-Банк.

## 📁 Файлы в этом наборе

### 1. **TZ_CFT_Compliance_Monitor.md** ⭐ ГЛАВНЫЙ ДОКУМЕНТ
Полное техническое задание (787 строк) включающее:
- Описание проекта и scope
- Все функциональные требования (F1–F5 модули)
- Структура БД с SQL
- API контракты с примерами
- Non-functional requirements
- Архитектура и tech stack
- 12-этапный план разработки
- Тестирование и acceptance criteria
- Deployment инструкции
- Context7 чек-лист

**Для кого?** Архитекторы, tech lead'ы, разработчики.

---

### 2. **SUMMARY_CFT_Compliance.md** 📊 КРАТКИЙ ОБЗОР
Сокращённая версия ТЗ (185 строк) с основным:
- Что это? Зачем?
- 5 ключевых функций (Dashboard, Таблицы, Импорт, CRUD, Экспорт)
- Tech stack одной таблицей
- Структура БД (кратко)
- API endpoints (таблица)
- 12 этапов разработки (сжато)
- Open questions

**Для кого?** Менеджеры, стейкхолдеры, быстрый обзор для разработчиков.

---

### 3. **MAPPING_REFERENCE.md** 🗺️ СПРАВОЧНИК МАППИНГА
Полный справочник (547 строк) для работы с Excel:
- Унифицированная схема БД (Python модель)
- Маппинг для каждого источника (6 таблиц):
  - Аренда Сейфов
  - Депозиты ФЛ
  - Депозиты ЮЛ
  - Кредиты ФЛ
  - Платежные поручения
  - Обработка платежей
- Примеры данных
- Python code snippets (парсер, валидатор, маппер)
- SQL для проверки импорта
- Таблица статусов и цветов

**Для кого?** Разработчики backend (сервис импорта Excel), ответственные за маппинг.

---

### 4. **QUICK_REFERENCE.md** ⚡ ШПАРГАЛКА
Быстрый справочник (~1000 строк) для разработчиков:
- 🚀 Быстрый старт (4 команды)
- 📊 Структура проекта (дерево папок)
- 🗄️ Database schema (полностью)
- 🔌 API endpoints (таблица со всеми методами)
- 🐍 Backend snippets (модели, schemas, CRUD, импорт Excel)
- ⚛️ Frontend snippets (таблица, dashboard, импорт, диалоги)
- 🧪 Testing (pytest fixtures, примеры)
- 🐳 Docker команды
- 🔄 Migration команды
- 📝 Environment variables
- 🔍 Debugging советы
- 📚 Полезные ссылки
- ✅ Чек-лист перед деплоем

**Для кого?** Разработчики (копировай-вставляй код!), DevOps.

---

## 🎯 Как использовать эти документы?

### Сценарий 1: Я архитектор / tech lead
1. Прочитай **SUMMARY_CFT_Compliance.md** (15 мин)
2. Пройдись по полному **TZ_CFT_Compliance_Monitor.md** (1-2 часа)
3. Поделись с командой части для каждого специалиста

### Сценарий 2: Я backend разработчик
1. Прочитай **SUMMARY_CFT_Compliance.md** (быстрый обзор)
2. Открой **QUICK_REFERENCE.md** (как шпаргалка)
3. Используй **MAPPING_REFERENCE.md** для сервиса импорта
4. Смотри **TZ_CFT_Compliance_Monitor.md** п. 5–7 (требования, БД, API)

### Сценарий 3: Я frontend разработчик
1. Прочитай **SUMMARY_CFT_Compliance.md**
2. Открой **QUICK_REFERENCE.md** для React snippets
3. Смотри **TZ_CFT_Compliance_Monitor.md** п. 5.2, 5.3, 5.4 (требования UI)
4. API endpoints есть в п. 7 и в QUICK_REFERENCE

### Сценарий 4: Я DevOps / настраиваю среду
1. **QUICK_REFERENCE.md** p. Docker Commands & Environment Variables
2. **TZ_CFT_Compliance_Monitor.md** п. 12 (Deployment & Operations)
3. Docker Compose файл в п. 12 (copy-paste)

### Сценарий 5: Я тестировщик / QA
1. **SUMMARY_CFT_Compliance.md** для понимания scope
2. **TZ_CFT_Compliance_Monitor.md** п. 11 (Testing & Acceptance Criteria)
3. **QUICK_REFERENCE.md** для примеров тестов

---

## 📊 Структура документов

```
TZ_CFT_Compliance_Monitor.md (ГЛАВНЫЙ)
├─ 1. Краткое описание проекта
├─ 2. Scope (in/out of scope)
├─ 3. Предположения и ограничения
├─ 4. User Flows (7 сценариев)
├─ 5. Функциональные требования (5 модулей × 6-7 требований)
├─ 6. Data Model (SQL для БД)
├─ 7. API Contract (9 endpoints с примерами)
├─ 8. Non-Functional Requirements
├─ 9. Architecture (диаграмма, стек, папки)
├─ 10. Development Plan (M1–M12, 4 недели)
├─ 11. Testing & Acceptance Criteria
├─ 12. Deployment & Operations (Docker, миграции, логирование)
├─ 13. Risks & Edge Cases
├─ 14. Context7 Checklist (10 items для дальнейшего уточнения)
└─ 15. Open Questions (6 вопросов)

SUMMARY_CFT_Compliance.md (КРАТКИЙ)
├─ Что это? + ключевые функции
├─ Tech stack (таблица)
├─ Структура БД
├─ API endpoints
├─ Plan (таблица с этапами)
├─ Open questions
└─ Ссылка на полное ТЗ

MAPPING_REFERENCE.md (СПРАВОЧНИК)
├─ Унифицированная схема
├─ 6 таблиц с маппингами
├─ Python code examples
├─ SQL queries
└─ Примеры данных

QUICK_REFERENCE.md (ШПАРГАЛКА)
├─ Quick start (4 команды)
├─ Все snippets (Python, React, SQL, Docker, etc.)
└─ Чек-листы
```

---

## 🎬 Быстрый старт (для разработчиков)

```bash
# 1. Клон проекта
git clone <repo>
cd compliance-monitor

# 2. Docker Compose (все сервисы)
docker-compose up -d

# 3. Миграции БД
docker exec compliance-monitor-backend alembic upgrade head

# 4. Открыть в браузере
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# Swagger:   http://localhost:8000/docs
```

---

## 📋 Чек-лист для начала разработки

- [ ] Все документы прочитаны (минимум — SUMMARY)
- [ ] Команда понимает scope и требования
- [ ] Backend разработчик знаком с MAPPING_REFERENCE
- [ ] Frontend разработчик знаком с требованиями UI в п. 5
- [ ] DevOps подготовил окружение (Docker, PostgreSQL)
- [ ] Git репо создан и настроен
- [ ] IDE/редакторы установлены (VS Code, PyCharm, etc.)
- [ ] Python 3.11+ и Node.js 18+ установлены локально
- [ ] Slack/Jira связаны для трекинга
- [ ] Первый sprint планируется (M1–M3)

---

## 🤔 Часто задаваемые вопросы

**Q: Нужна ли авторизация?**  
A: В ТЗ её нет (public проект). Если нужна — см. Open Questions п. 15.

**Q: Можно ли использовать другой фреймворк?**  
A: FastAPI + SQLAlchemy + React — рекомендуемые. Другие стеки возможны, но требуют согласования.

**Q: Какой размер команды оптимален?**  
A: 1–2 backend, 1–2 frontend, 1 DevOps/QA. 4 недели разработки на эту команду.

**Q: Можно ли распределить на более долгий срок?**  
A: Да, разбей на спринты по 2 недели (М1–М3, потом М4–М6, и т.д.).

**Q: Как импортировать данные из других источников (не Excel)?**  
A: Расширь маппер в `services/excel_mapper.py` или добавь новый endpoint.

**Q: Есть ли API для интеграции с другими системами?**  
A: Да, все endpoints в п. 7 ТЗ готовы к интеграции. Out of scope — авторизация.

---

## 📞 Контакты

- **Questions about requirements?** → см. п. 15 (Open Questions) в TZ_CFT_Compliance_Monitor.md
- **Need code examples?** → QUICK_REFERENCE.md
- **Excel mapping?** → MAPPING_REFERENCE.md
- **High-level understanding?** → SUMMARY_CFT_Compliance.md

---

## 📈 Метрики успеха

✅ **MVP (4 недели):**
- Dashboard отображается корректно
- Импорт из Excel работает
- CRUD операции работают
- Все endpoints тестируются

✅ **Production (6–8 недель):**
- Авторизация (если нужна)
- История версий
- Сложные фильтры
- Экспорт в различные форматы

✅ **Масштабирование:**
- Поддержка 50k+ записей
- Асинхронный импорт
- Кэширование
- Оптимизация запросов

---

## 📝 Версионирование документов

| Документ | Версия | Дата | Статус |
|----------|--------|------|--------|
| TZ_CFT_Compliance_Monitor.md | 1.0 | 12.12.2025 | ✅ Ready |
| SUMMARY_CFT_Compliance.md | 1.0 | 12.12.2025 | ✅ Ready |
| MAPPING_REFERENCE.md | 1.0 | 12.12.2025 | ✅ Ready |
| QUICK_REFERENCE.md | 1.0 | 12.12.2025 | ✅ Ready |

---

## 🎓 Рекомендуемый порядок изучения

1. **Менеджер проекта:** SUMMARY (15 мин) → TZ разделы 1–4 (1 час)
2. **Tech Lead:** Все документы (3–4 часа) → распредели по команде
3. **Backend:** SUMMARY → QUICK_REFERENCE → MAPPING_REFERENCE → TZ разделы 5–7
4. **Frontend:** SUMMARY → QUICK_REFERENCE → TZ раздел 5.2–5.4
5. **DevOps:** QUICK_REFERENCE → TZ раздел 12
6. **QA:** TZ раздел 11 → QUICK_REFERENCE (тесты)

---

**Готово к разработке! 🚀**

*Если есть вопросы или нужны уточнения — см. Open Questions в TZ или свяжись с архитектором.*

