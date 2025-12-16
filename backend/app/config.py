from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    environment: str = "development"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://compliance:compliance123@postgres:5432/compliance_db"
    )
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    cors_origins: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> any:
            if field_name == 'cors_origins':
                # Парсим JSON массив из строки
                import json
                try:
                    return json.loads(raw_val)
                except:
                    return [raw_val] if raw_val else ["http://localhost:3000"]
            return cls.json_schema_extra.get(field_name, raw_val)


settings = Settings()

