from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import uuid
import openpyxl
from io import BytesIO
from app.db.database import get_db
from app.models.process_record import ProcessRecord
from app.models.import_log import ImportLog
from app.schemas.import_schema import ImportResponse, ImportLogResponse
from app.services.excel_mapper import (
    detect_source,
    map_excel_row_to_record,
    normalize_column_name,
    TableSourceEnum
)
from app.services.validation import validate_record, ValidationError

router = APIRouter(prefix="/api/import", tags=["import"])


@router.post("/excel", response_model=ImportResponse, status_code=202)
async def import_excel_file(
    file: UploadFile = File(...),
    table_source: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Импортирует данные из Excel файла.
    
    Args:
        file: Excel файл для импорта
        table_source: Опциональный источник таблицы (подсказка для детектирования)
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=415,
            detail="File must be Excel format (.xlsx or .xls)"
        )
    
    # Генерируем batch_id
    import_batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    try:
        # Читаем файл
        contents = await file.read()
        wb = openpyxl.load_workbook(BytesIO(contents))
        ws = wb.active
        
        # Получаем заголовки
        headers = [cell.value for cell in ws[1] if cell.value]
        
        if not headers:
            raise HTTPException(
                status_code=400,
                detail="Excel file must have headers in the first row"
            )
        
        # Детектируем источник
        final_table_source = None
        source = None
        
        try:
            # Если передан table_source, используем его (может быть любым строковым значением для динамических чек-листов)
            if table_source:
                # Проверяем, является ли это стандартным источником
                if table_source in [e.value for e in TableSourceEnum]:
                    source = TableSourceEnum(table_source)
                    final_table_source = source.value
                    print(f"Using provided standard table_source: {table_source}")
                else:
                    # Для динамических чек-листов используем строку напрямую
                    final_table_source = table_source
                    # Для маппинга используем SAFES_RENTAL как базовый (универсальный формат)
                    source = TableSourceEnum.SAFES_RENTAL
                    print(f"Using provided dynamic table_source: {table_source}")
            else:
                source = detect_source(headers)
                final_table_source = source.value
                print(f"Auto-detected source: {source.value}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Обрабатываем строки
        errors = []
        success_count = 0
        total_rows = 0
        processed_rows = set()  # Для отслеживания уже обработанных строк и предотвращения дубликатов
        
        # Используем max_row для ограничения количества обрабатываемых строк
        # Игнорируем скрытые строки и используем только видимые данные
        max_row = ws.max_row
        
        # Собираем все строки сначала, чтобы избежать проблем с итератором
        rows_to_process = []
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True, max_row=max_row), start=2):
            # Пропускаем пустые строки
            if not any(row):
                continue
            
            # Создаём словарь данных строки (с оригинальными заголовками)
            row_data = {}
            for col_idx, header in enumerate(headers):
                if col_idx < len(row):
                    row_data[header] = row[col_idx]
            
            # Создаём уникальный ключ для строки на основе всех значений для проверки дубликатов
            # Используем строковое представление всех значений для более надежной проверки
            row_values_str = '|'.join(
                str(v).strip().lower() if v is not None else ''
                for v in row[:len(headers)]
            )
            row_key = f"{final_table_source}:{row_values_str}"
            
            # Проверяем, не обрабатывали ли мы уже эту строку
            if row_key in processed_rows:
                print(f"SKIPPING DUPLICATE ROW {row_idx}: {row_data.get(headers[0] if headers else 'unknown', 'N/A')}")
                continue
            
            processed_rows.add(row_key)
            rows_to_process.append((row_idx, row_data))
            total_rows += 1
        
        # Теперь обрабатываем собранные строки
        for row_idx, row_data in rows_to_process:
            
            # Детальное логирование для отладки
            print(f"\n{'='*80}")
            print(f"ROW {row_idx} - RAW DATA:")
            for key, value in row_data.items():
                if value is not None:
                    print(f"  {key}: {repr(value)} (type: {type(value).__name__})")
            print(f"{'='*80}")
            
            # Маппируем на структуру БД (передаём оригинальный row_data)
            try:
                record_data = map_excel_row_to_record(
                    row_data,
                    source,
                    headers
                )
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                print(f"Mapping error at row {row_idx}: {str(e)}")
                print(f"Row data: {row_data}")
                print(f"Traceback: {error_trace}")
                errors.append(ValidationError(
                    row_idx,
                    "mapping",
                    f"Mapping error: {str(e)}"
                ))
                continue
            
            # Валидируем (используем final_table_source для динамических чек-листов)
            is_valid, validation_errors = validate_record(record_data, final_table_source, row_idx)
            
            if not is_valid:
                # Логируем проблемные данные для отладки
                if any(err.field == 'status' for err in validation_errors):
                    print(f"Row {row_idx} status validation error:")
                    print(f"  Original row data: {row_data}")
                    print(f"  Mapped record_data: {record_data}")
                    print(f"  Status value: {repr(record_data.get('status'))}")
                errors.extend(validation_errors)
                continue
            
            # Сохраняем в БД (используем final_table_source)
            try:
                # Заменяем table_source на финальный (для динамических чек-листов)
                record_data['table_source'] = final_table_source
                
                # Проверяем, не существует ли уже такая запись в БД
                # Проверяем по process_name, table_source и другим ключевым полям для более надежной проверки
                query = db.query(ProcessRecord).filter(
                    ProcessRecord.process_name == record_data.get('process_name'),
                    ProcessRecord.table_source == final_table_source,
                    ProcessRecord.is_archived == False
                )
                
                # Дополнительная проверка по product_type, если оно есть
                if record_data.get('product_type'):
                    query = query.filter(ProcessRecord.product_type == record_data.get('product_type'))
                
                existing_record = query.first()
                
                if existing_record:
                    # Если запись уже существует, пропускаем её (не создаём дубликат)
                    print(f"SKIPPING EXISTING RECORD at row {row_idx}: {record_data.get('process_name')}")
                    continue
                
                db_record = ProcessRecord(
                    **record_data,
                    import_batch_id=import_batch_id,
                    import_date=datetime.utcnow()
                )
                db.add(db_record)
                success_count += 1
            except Exception as e:
                errors.append(ValidationError(
                    row_idx,
                    "database",
                    f"Database error: {str(e)}"
                ))
        
        # Коммитим изменения
        db.commit()
        
        # Логируем импорт
        import_log = ImportLog(
            import_batch_id=import_batch_id,
            filename=file.filename,
            table_source=final_table_source,
            total_rows=total_rows,
            success_rows=success_count,
            error_rows=len(errors),
            error_details=[e.to_dict() for e in errors[:100]],  # Ограничиваем размер
            imported_at=datetime.utcnow()
        )
        db.add(import_log)
        db.commit()
        
        return ImportResponse(
            import_batch_id=import_batch_id,
            total_rows=total_rows,
            success_rows=success_count,
            error_rows=len(errors),
            errors=[e.to_dict() for e in errors[:50]]  # Возвращаем первые 50 ошибок
        )
    
    except Exception as e:
        db.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"Import error: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"Import failed: {str(e)}"
        )


@router.get("/logs", response_model=list[ImportLogResponse])
def get_import_logs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Получить историю импортов"""
    logs = (
        db.query(ImportLog)
        .order_by(ImportLog.imported_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [ImportLogResponse.model_validate(log) for log in logs]

