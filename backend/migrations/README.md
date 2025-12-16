# Alembic Migrations

Для создания и применения миграций используйте следующие команды:

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Описание изменений"

# Применить все миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Просмотреть текущую версию
alembic current

# Просмотреть историю
alembic history
```

