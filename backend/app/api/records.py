from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from app.db.database import get_db
from app.schemas.record_schema import (
    ProcessRecordCreate,
    ProcessRecordUpdate,
    ProcessRecordResponse,
    ProcessRecordListResponse
)
from app.services.record_service import (
    get_records,
    get_record_by_id,
    create_record,
    update_record,
    delete_record,
    bulk_delete_records
)

router = APIRouter(prefix="/api/records", tags=["records"])


@router.get("", response_model=ProcessRecordListResponse)
def read_records(
    table_source: Optional[str] = Query(None, description="Фильтр по источнику"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    search: Optional[str] = Query(None, description="Поиск по названию процесса"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Получить список записей с фильтрацией и пагинацией"""
    records, total = get_records(
        db=db,
        table_source=table_source,
        status=status,
        skip=skip,
        limit=limit,
        search=search
    )
    return ProcessRecordListResponse(
        records=[ProcessRecordResponse.model_validate(r) for r in records],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{record_id}", response_model=ProcessRecordResponse)
def read_record(record_id: UUID, db: Session = Depends(get_db)):
    """Получить запись по ID"""
    record = get_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return ProcessRecordResponse.model_validate(record)


@router.post("", response_model=ProcessRecordResponse, status_code=201)
def create_new_record(record: ProcessRecordCreate, db: Session = Depends(get_db)):
    """Создать новую запись"""
    return create_record(db, record)


@router.put("/{record_id}", response_model=ProcessRecordResponse)
def update_existing_record(
    record_id: UUID,
    record_update: ProcessRecordUpdate,
    db: Session = Depends(get_db)
):
    """Обновить запись"""
    updated_record = update_record(db, record_id, record_update)
    if not updated_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return ProcessRecordResponse.model_validate(updated_record)


@router.delete("/{record_id}", status_code=204)
def delete_existing_record(record_id: UUID, db: Session = Depends(get_db)):
    """Удалить запись"""
    success = delete_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return None


@router.post("/bulk-delete", status_code=200)
def bulk_delete_existing_records(
    record_ids: List[UUID],
    db: Session = Depends(get_db)
):
    """Удалить несколько записей"""
    if not record_ids:
        raise HTTPException(status_code=400, detail="No record IDs provided")
    
    deleted_count = bulk_delete_records(db, record_ids)
    return {"deleted": deleted_count}

