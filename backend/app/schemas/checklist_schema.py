from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ChecklistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    table_source: str = Field(..., max_length=100)


class ChecklistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class ChecklistResponse(BaseModel):
    id: UUID
    name: str
    table_source: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

