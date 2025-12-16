"""
Сервис для работы с записями процессов
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from uuid import UUID
from app.models.process_record import ProcessRecord
from app.schemas.record_schema import ProcessRecordCreate, ProcessRecordUpdate


def get_records(
    db: Session,
    table_source: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> tuple[List[ProcessRecord], int]:
    """
    Получить список записей с фильтрацией и пагинацией.
    
    Returns:
        tuple: (список записей, общее количество)
    """
    query = db.query(ProcessRecord).filter(ProcessRecord.is_archived == False)
    
    if table_source:
        query = query.filter(ProcessRecord.table_source == table_source)
    
    if status:
        query = query.filter(ProcessRecord.status == status)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(ProcessRecord.process_name.ilike(search_pattern))
    
    total = query.count()
    records = query.offset(skip).limit(limit).all()
    
    return records, total


def get_record_by_id(db: Session, record_id: UUID) -> Optional[ProcessRecord]:
    """Получить запись по ID"""
    return db.query(ProcessRecord).filter(ProcessRecord.id == record_id).first()


def create_record(db: Session, record: ProcessRecordCreate) -> ProcessRecord:
    """Создать новую запись"""
    db_record = ProcessRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_record(
    db: Session,
    record_id: UUID,
    record_update: ProcessRecordUpdate
) -> Optional[ProcessRecord]:
    """Обновить запись"""
    db_record = get_record_by_id(db, record_id)
    if not db_record:
        return None
    
    update_data = record_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_record(db: Session, record_id: UUID) -> bool:
    """Удалить запись"""
    db_record = get_record_by_id(db, record_id)
    if not db_record:
        return False
    
    db.delete(db_record)
    db.commit()
    return True


def bulk_delete_records(db: Session, record_ids: List[UUID]) -> int:
    """Удалить несколько записей"""
    deleted = db.query(ProcessRecord).filter(ProcessRecord.id.in_(record_ids)).delete(synchronize_session=False)
    db.commit()
    return deleted


def get_dashboard_summary(db: Session) -> dict:
    """
    Получить сводку для dashboard: общий прогресс, кол-во по статусам, по источникам.
    Фильтрует только активные чек-листы (не показывает удаленные).
    """
    from app.models.checklist import Checklist
    
    # Получаем список активных table_source из checklists
    active_table_sources = set()
    try:
        active_checklists = db.query(Checklist).filter(Checklist.is_active == True).all()
        active_table_sources = {c.table_source for c in active_checklists}
    except Exception:
        # Если таблица не существует, продолжаем без фильтрации по активным чек-листам
        pass
    
    # Получаем список неактивных чек-листов (удаленных)
    inactive_table_sources = set()
    try:
        inactive_checklists = db.query(Checklist).filter(Checklist.is_active == False).all()
        inactive_table_sources = {c.table_source for c in inactive_checklists}
    except Exception:
        pass
    
    # Получаем уникальные table_source из process_records (виртуальные чек-листы)
    virtual_sources = set()
    try:
        unique_sources = db.query(ProcessRecord.table_source).distinct().all()
        virtual_sources = {s[0] for s in unique_sources}
    except Exception:
        pass
    
    # Формируем список разрешенных источников:
    # 1. Активные чек-листы из таблицы checklists
    # 2. Виртуальные чек-листы (есть записи, но нет в checklists), НО не удаленные
    allowed_sources = active_table_sources.copy()
    for source in virtual_sources:
        if source not in inactive_table_sources:
            allowed_sources.add(source)
    
    # Если нет активных источников, используем все (для обратной совместимости)
    if not allowed_sources:
        allowed_sources = None
    
    # Общая статистика (только по активным источникам)
    total_query = db.query(ProcessRecord).filter(ProcessRecord.is_archived == False)
    if allowed_sources is not None:
        total_query = total_query.filter(ProcessRecord.table_source.in_(allowed_sources))
    total_records = total_query.count()
    
    # Статистика по статусам (только по активным источникам)
    status_query = (
        db.query(
            ProcessRecord.status,
            func.count(ProcessRecord.id).label('count')
        )
        .filter(ProcessRecord.is_archived == False)
    )
    if allowed_sources is not None:
        status_query = status_query.filter(ProcessRecord.table_source.in_(allowed_sources))
    
    status_stats = status_query.group_by(ProcessRecord.status).all()
    
    completed = 0
    in_progress = 0
    not_started = 0
    
    for status, count in status_stats:
        if status in ['Выполнено', 'Успешно']:
            completed += count
        elif status == 'В работе':
            in_progress += count
        elif status == 'Не начато':
            not_started += count
    
    # Процент выполнения
    progress_percent = (completed / total_records * 100) if total_records > 0 else 0.0
    
    # Статистика по источникам (только по активным источникам)
    source_query = (
        db.query(
            ProcessRecord.table_source,
            ProcessRecord.status,
            func.count(ProcessRecord.id).label('count')
        )
        .filter(ProcessRecord.is_archived == False)
    )
    if allowed_sources is not None:
        source_query = source_query.filter(ProcessRecord.table_source.in_(allowed_sources))
    
    source_stats = source_query.group_by(ProcessRecord.table_source, ProcessRecord.status).all()
    
    by_source = {}
    for table_source, status, count in source_stats:
        if table_source not in by_source:
            by_source[table_source] = {
                'total': 0,
                'completed': 0,
                'in_progress': 0,
                'not_started': 0
            }
        
        by_source[table_source]['total'] += count
        if status in ['Выполнено', 'Успешно']:
            by_source[table_source]['completed'] += count
        elif status == 'В работе':
            by_source[table_source]['in_progress'] += count
        elif status == 'Не начато':
            by_source[table_source]['not_started'] += count
    
    return {
        'total_records': total_records,
        'completed': completed,
        'in_progress': in_progress,
        'not_started': not_started,
        'progress_percent': round(progress_percent, 2),
        'by_source': by_source
    }

