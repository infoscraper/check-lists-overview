from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class ProcessRecordBase(BaseModel):
    process_name: str = Field(..., min_length=1, max_length=255)
    product_type: Optional[str] = Field(None, max_length=100)
    status: str = Field(..., max_length=50)
    date_kb: Optional[date] = None
    fio_customer: Optional[str] = Field(None, max_length=255)
    date_bank_receipt: Optional[date] = None
    fio_bank_officer: Optional[str] = Field(None, max_length=255)
    process_number: Optional[int] = None
    bank_employee_name: Optional[str] = Field(None, max_length=255)
    comments: Optional[str] = None
    table_source: str = Field(..., max_length=100)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_statuses = ["Выполнено", "Успешно", "В работе", "Не начато", "Не успешно"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v

    @field_validator("table_source")
    @classmethod
    def validate_table_source(cls, v: str) -> str:
        # Убрали жесткую валидацию, чтобы можно было создавать динамические чек-листы
        # Проверяем только формат
        if not v or len(v) > 100:
            raise ValueError("table_source must be between 1 and 100 characters")
        return v


class ProcessRecordCreate(ProcessRecordBase):
    pass


class ProcessRecordUpdate(BaseModel):
    process_name: Optional[str] = Field(None, min_length=1, max_length=255)
    product_type: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=50)
    date_kb: Optional[date] = None
    fio_customer: Optional[str] = Field(None, max_length=255)
    date_bank_receipt: Optional[date] = None
    fio_bank_officer: Optional[str] = Field(None, max_length=255)
    process_number: Optional[int] = None
    bank_employee_name: Optional[str] = Field(None, max_length=255)
    comments: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        valid_statuses = ["Выполнено", "Успешно", "В работе", "Не начато", "Не успешно"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v


class ProcessRecordResponse(ProcessRecordBase):
    id: UUID
    import_date: Optional[datetime] = None
    import_batch_id: Optional[str] = None
    is_archived: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProcessRecordListResponse(BaseModel):
    records: list[ProcessRecordResponse]
    total: int
    skip: int
    limit: int

