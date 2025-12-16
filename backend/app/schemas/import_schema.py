from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ImportError(BaseModel):
    row: int
    field: str
    message: str


class ImportResponse(BaseModel):
    import_batch_id: str
    total_rows: int
    success_rows: int
    error_rows: int
    errors: List[ImportError]


class ImportLogResponse(BaseModel):
    id: str
    import_batch_id: str
    filename: Optional[str]
    table_source: Optional[str]
    total_rows: int
    success_rows: int
    error_rows: int
    imported_at: datetime

    class Config:
        from_attributes = True

