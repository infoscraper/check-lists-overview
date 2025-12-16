"""
Валидация данных перед сохранением в БД
"""
from typing import Tuple, List, Optional
from datetime import date
from app.services.excel_mapper import StatusEnum, TableSourceEnum


class ValidationError:
    def __init__(self, row: int, field: str, message: str):
        self.row = row
        self.field = field
        self.message = message
    
    def __repr__(self):
        return f"Row {self.row}, Field '{self.field}': {self.message}"
    
    def to_dict(self):
        return {
            "row": self.row,
            "field": self.field,
            "message": self.message
        }


def validate_record(data: dict, source: str, row: int = 0) -> Tuple[bool, List[ValidationError]]:
    """
    Валидирует одну запись перед сохранением.
    
    Args:
        data: словарь с данными записи
        source: источник таблицы
        row: номер строки (для ошибок)
    
    Returns:
        Tuple[bool, List[ValidationError]]: (валидна ли запись, список ошибок)
    """
    errors = []
    
    # Обязательные поля
    if not data.get('process_name') or not str(data['process_name']).strip():
        errors.append(ValidationError(row, 'process_name', 'Required field'))
    
    if not data.get('status'):
        errors.append(ValidationError(row, 'status', 'Required field'))
    else:
        valid_statuses = [e.value for e in StatusEnum]
        if data['status'] not in valid_statuses:
            errors.append(ValidationError(
                row, 'status',
                f"Must be one of: {', '.join(valid_statuses)}"
            ))
    
    if not data.get('table_source'):
        errors.append(ValidationError(row, 'table_source', 'Required field'))
    else:
        valid_sources = [e.value for e in TableSourceEnum]
        if data['table_source'] not in valid_sources:
            errors.append(ValidationError(
                row, 'table_source',
                f"Must be one of: {', '.join(valid_sources)}"
            ))
    
    # Валидация дат
    for date_field in ['date_kb', 'date_bank_receipt']:
        if data.get(date_field):
            value = data[date_field]
            if isinstance(value, str):
                try:
                    # Проверяем формат YYYY-MM-DD
                    date.fromisoformat(value)
                except ValueError:
                    errors.append(ValidationError(
                        row, date_field,
                        f"Invalid date format. Expected YYYY-MM-DD, got: {value}"
                    ))
            elif not isinstance(value, (date, type(None))):
                errors.append(ValidationError(
                    row, date_field,
                    f"Invalid date type: {type(value)}"
                ))
    
    # Валидация process_number
    if data.get('process_number') is not None:
        try:
            int(data['process_number'])
        except (ValueError, TypeError):
            errors.append(ValidationError(
                row, 'process_number',
                f"Must be an integer, got: {data['process_number']}"
            ))
    
    return len(errors) == 0, errors

