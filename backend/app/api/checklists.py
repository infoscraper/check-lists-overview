from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.database import get_db
from app.schemas.checklist_schema import ChecklistCreate, ChecklistResponse
from app.services.checklist_service import (
    get_all_checklists,
    create_checklist,
    get_checklist_by_table_source,
    delete_checklist,
    bulk_delete_checklists
)

router = APIRouter(prefix="/api/checklists", tags=["checklists"])


@router.get("", response_model=List[ChecklistResponse])
def get_checklists(
    include_virtual: bool = Query(True, description="Включить виртуальные чек-листы"),
    db: Session = Depends(get_db)
):
    """Получить список всех чек-листов"""
    checklists = get_all_checklists(db, include_virtual=include_virtual)
    return checklists


@router.get("/real", response_model=List[ChecklistResponse])
def get_real_checklists(db: Session = Depends(get_db)):
    """Получить список только реальных чек-листов (созданных пользователем)"""
    checklists = get_all_checklists(db, include_virtual=False)
    return checklists


@router.post("", response_model=ChecklistResponse, status_code=201)
def create_new_checklist(
    checklist_data: ChecklistCreate,
    db: Session = Depends(get_db)
):
    """Создать новый чек-лист"""
    try:
        checklist = create_checklist(db, checklist_data.name)
        return checklist
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания чек-листа: {str(e)}")


@router.delete("/{checklist_id}", status_code=204)
def delete_checklist_by_id(
    checklist_id: UUID,
    db: Session = Depends(get_db)
):
    """Удалить чек-лист по ID"""
    success = delete_checklist(db, checklist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Чек-лист не найден")
    return None


@router.post("/bulk-delete", status_code=204)
def bulk_delete_checklists_endpoint(
    checklist_ids: List[UUID],
    db: Session = Depends(get_db)
):
    """Удалить несколько чек-листов"""
    if not checklist_ids:
        raise HTTPException(status_code=400, detail="Список ID не может быть пустым")
    
    deleted_count = bulk_delete_checklists(db, checklist_ids)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Чек-листы не найдены")
    return None
