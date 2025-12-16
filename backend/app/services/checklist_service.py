"""
Сервис для работы с чек-листами
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import re
from app.models.checklist import Checklist


def generate_table_source(name: str) -> str:
    """
    Генерирует table_source из названия чек-листа.
    Преобразует кириллицу в латиницу и создает slug.
    """
    # Простая транслитерация
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    
    # Транслитерация
    result = ''
    for char in name:
        if char in translit_map:
            result += translit_map[char]
        elif char.isalnum() or char in ['-', '_']:
            result += char
        else:
            result += '_'
    
    # Приводим к lowercase и заменяем пробелы на подчеркивания
    result = result.lower().strip()
    result = re.sub(r'[^a-z0-9_-]', '', result)
    result = re.sub(r'[-_]+', '_', result)
    result = re.sub(r'^[-_]+|[-_]+$', '', result)
    
    # Если пусто, используем fallback
    if not result:
        result = 'checklist_' + str(hash(name) % 10000)
    
    return result


def get_all_checklists(db: Session, include_virtual: bool = True) -> List[Checklist]:
    """Получить все активные чек-листы из БД и виртуальные из process_records"""
    from app.models.process_record import ProcessRecord
    import uuid
    from datetime import datetime
    
    # Получаем чек-листы из таблицы checklists (только реальные, созданные пользователем)
    try:
        db_checklists = db.query(Checklist).filter(Checklist.is_active == True).all()
    except Exception:
        # Если таблица не существует, возвращаем пустой список
        db_checklists = []
    
    # Получаем уникальные table_source из активных чек-листов
    existing_sources = {c.table_source for c in db_checklists}
    all_checklists = list(db_checklists)
    
    # Получаем список всех неактивных чек-листов (чтобы не показывать их как виртуальные)
    inactive_sources = set()
    try:
        inactive_checklists = db.query(Checklist).filter(Checklist.is_active == False).all()
        inactive_sources = {c.table_source for c in inactive_checklists}
    except Exception:
        pass
    
    # Создаем мапу всех чек-листов (включая неактивные) для получения названий
    # Также создаем обратную мапу: если table_source похож, используем название
    all_checklists_map = {}
    all_checklists_by_name = {}
    try:
        all_db_checklists = db.query(Checklist).all()
        for cl in all_db_checklists:
            all_checklists_map[cl.table_source] = cl.name
            # Создаем нормализованный ключ для поиска
            normalized_source = cl.table_source.lower().replace('_', '').replace('-', '')
            all_checklists_by_name[normalized_source] = cl.name
    except Exception:
        pass
    
    # Если нужно включить виртуальные (для отображения), добавляем их
    if include_virtual:
        try:
            unique_sources = db.query(ProcessRecord.table_source).distinct().all()
            
            # Добавляем виртуальные чек-листы для table_source, которые есть в process_records, но нет в активных checklists
            # НО не добавляем, если этот table_source есть в неактивных чек-листах (удаленные чек-листы не показываем)
            for source_tuple in unique_sources:
                source = source_tuple[0]
                # Пропускаем, если чек-лист уже есть в активных или если он был удален (неактивен)
                if source not in existing_sources and source not in inactive_sources:
                    # Используем название из мапы всех чек-листов, если оно есть
                    name = all_checklists_map.get(source, source)
                    
                    # Если не нашли точное совпадение, пытаемся найти по нормализованному ключу
                    if name == source:
                        normalized_source = source.lower().replace('_', '').replace('-', '')
                        name = all_checklists_by_name.get(normalized_source, source)
                    
                    virtual_checklist = Checklist(
                        id=uuid.uuid4(),
                        name=name,
                        table_source=source,
                        is_active=True,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    all_checklists.append(virtual_checklist)
                    existing_sources.add(source)
        except Exception:
            pass  # Игнорируем ошибки при запросе process_records
    
    # Сортируем по названию
    all_checklists.sort(key=lambda x: x.name)
    return all_checklists


def get_checklist_by_table_source(db: Session, table_source: str) -> Optional[Checklist]:
    """Получить чек-лист по table_source"""
    return db.query(Checklist).filter(Checklist.table_source == table_source).first()


def delete_checklist(db: Session, checklist_id: UUID) -> bool:
    """Удалить чек-лист (пометить как неактивный)"""
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not checklist:
        return False
    
    # Помечаем как неактивный вместо физического удаления
    checklist.is_active = False
    db.commit()
    return True


def bulk_delete_checklists(db: Session, checklist_ids: List[UUID]) -> int:
    """Удалить несколько чек-листов"""
    deleted = db.query(Checklist).filter(
        Checklist.id.in_(checklist_ids)
    ).update({"is_active": False}, synchronize_session=False)
    db.commit()
    return deleted


def create_checklist(db: Session, name: str) -> Checklist:
    """Создать новый чек-лист"""
    # Нормализуем название (убираем лишние пробелы)
    name = name.strip()
    if not name:
        raise ValueError("Название чек-листа не может быть пустым")
    
    # Проверяем уникальность названия (только среди активных)
    existing_active = db.query(Checklist).filter(
        Checklist.name == name,
        Checklist.is_active == True
    ).first()
    if existing_active:
        raise ValueError(f"Чек-лист с названием '{name}' уже существует")
    
    # Если есть неактивный чек-лист с таким же названием, удаляем его полностью
    # чтобы можно было создать новый с тем же названием
    existing_inactive = db.query(Checklist).filter(
        Checklist.name == name,
        Checklist.is_active == False
    ).all()
    if existing_inactive:
        for inactive_checklist in existing_inactive:
            db.delete(inactive_checklist)
        db.commit()
    
    # Генерируем table_source
    base_table_source = generate_table_source(name)
    table_source = base_table_source
    
    # Проверяем уникальность table_source и добавляем суффикс если нужно
    counter = 1
    while db.query(Checklist).filter(
        Checklist.table_source == table_source,
        Checklist.is_active == True
    ).first():
        table_source = f"{base_table_source}_{counter}"
        counter += 1
        # Защита от бесконечного цикла
        if counter > 1000:
            raise ValueError("Не удалось создать уникальный table_source")
    
    checklist = Checklist(name=name, table_source=table_source)
    db.add(checklist)
    db.commit()
    db.refresh(checklist)
    return checklist

