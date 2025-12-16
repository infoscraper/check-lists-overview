from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import records, dashboard, import_excel, export, checklists
from app.db.database import engine, Base

# Создаём таблицы при старте (в продакшене используйте миграции)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Чек-листы ЦФТ API",
    description="API для системы мониторинга прогресса процессов ЦФТ-Банк",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(records.router)
app.include_router(dashboard.router)
app.include_router(import_excel.router)
app.include_router(export.router)
app.include_router(checklists.router)


@app.get("/")
def root():
    return {
        "message": "Чек-листы ЦФТ API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}

