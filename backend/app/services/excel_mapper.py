"""
Сервис для маппинга колонок Excel на унифицированную схему БД
"""
from typing import Dict, Tuple, Optional
from enum import Enum
from datetime import datetime
import re


class TableSourceEnum(str, Enum):
    SAFES_RENTAL = "safes_rental"
    DEPOSITS_FL = "deposits_fl"
    DEPOSITS_UL = "deposits_ul"
    CREDITS_FL = "credits_fl"
    PAYMENT_ORDERS = "payment_orders"
    PAYMENT_PROCESSING = "payment_processing"


class StatusEnum(str, Enum):
    COMPLETED = "Выполнено"
    SUCCESS = "Успешно"
    IN_PROGRESS = "В работе"
    NOT_STARTED = "Не начато"
    FAILED = "Не успешно"


# Маппинги колонок Excel на поля БД
COLUMN_MAPPINGS = {
    TableSourceEnum.SAFES_RENTAL: {
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'дата кб': 'date_kb',
        'дата кв': 'date_kb',  # альтернативное написание
        'фио': 'fio_customer',
        'дата приемки банк': 'date_bank_receipt',
        'фио от банка': 'fio_bank_officer',
        'комментарии': 'comments',  # добавлено для поддержки колонки комментариев
        'комментарий': 'comments',
    },
    TableSourceEnum.DEPOSITS_FL: {
        'нпп': 'process_number',
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'дата приемки': 'date_bank_receipt',
        'фио от банка': 'fio_bank_officer',
        'комментарий': 'comments',
    },
    TableSourceEnum.DEPOSITS_UL: {
        'наименование процесса': 'process_name',
        'статус': 'status',
        'комментарий': 'comments',
    },
    TableSourceEnum.CREDITS_FL: {
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'дата кб': 'date_kb',
        'дата кв': 'date_kb',  # альтернативное написание
        'стойбец': 'bank_employee_name',
        'стойлец': 'bank_employee_name',  # альтернативное написание
        'столбец1': 'bank_employee_name',  # альтернативное написание из Excel
        'столбец': 'bank_employee_name',  # альтернативное написание
        'фио кб': 'fio_bank_officer',
        'фио кв': 'fio_bank_officer',  # альтернативное написание
        'фио  кв': 'fio_bank_officer',  # с двойным пробелом
        'дата приемки банк': 'date_bank_receipt',
        'дата приемки': 'date_bank_receipt',
        'фио от банка': 'fio_bank_officer',
    },
    TableSourceEnum.PAYMENT_ORDERS: {
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'комментарий': 'comments',
    },
    TableSourceEnum.PAYMENT_PROCESSING: {
        'наименование процесса': 'process_name',
        'продукт': 'product_type',
        'статус': 'status',
        'комментарий': 'comments',
    },
}


def normalize_column_name(col_name: str) -> str:
    """Нормализует название колонки для сравнения (lowercase, убирает пробелы)"""
    if not col_name:
        return ""
    # Убираем все пробелы (в начале, конце и внутри) и приводим к lowercase
    normalized = str(col_name).strip().lower()
    # Убираем множественные пробелы внутри
    normalized = ' '.join(normalized.split())
    return normalized


def detect_source(excel_columns: list) -> TableSourceEnum:
    """
    Автоматически определяет источник таблицы на основе набора колонок.
    Использует гибкое сопоставление по ключевым колонкам.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    excel_cols_normalized = [normalize_column_name(str(col)) for col in excel_columns if col]
    excel_cols_set = set(excel_cols_normalized)
    
    # Логирование для отладки
    logger.info(f"Detecting source from columns: {excel_columns}")
    logger.info(f"Normalized columns: {list(excel_cols_set)}")
    
    # Определяем ключевые колонки для каждого источника
    # (не все колонки обязательны, только ключевые)
    source_key_columns = {
        TableSourceEnum.SAFES_RENTAL: {
            'наименование процесса', 'продукт', 'статус', 
            'дата кб', 'дата кв', 'фио', 'дата приемки банк', 'фио от банка'
        },
        TableSourceEnum.DEPOSITS_FL: {
            'нпп', 'наименование процесса', 'продукт', 'статус'
        },
        TableSourceEnum.DEPOSITS_UL: {
            'наименование процесса', 'статус'
        },
        TableSourceEnum.CREDITS_FL: {
            'наименование процесса', 'продукт', 'статус', 
            'дата кб', 'дата кв', 'стойбец', 'стойлец'
        },
        TableSourceEnum.PAYMENT_ORDERS: {
            'наименование процесса', 'продукт', 'статус'
        },
        TableSourceEnum.PAYMENT_PROCESSING: {
            'наименование процесса', 'продукт', 'статус'
        },
    }
    
    # Минимальные обязательные колонки для каждого источника
    source_min_required = {
        TableSourceEnum.SAFES_RENTAL: {'наименование процесса', 'статус', 'продукт'},
        TableSourceEnum.DEPOSITS_FL: {'наименование процесса', 'статус', 'нпп'},
        TableSourceEnum.DEPOSITS_UL: {'наименование процесса', 'статус'},
        TableSourceEnum.CREDITS_FL: {'наименование процесса', 'статус', 'продукт'},
        TableSourceEnum.PAYMENT_ORDERS: {'наименование процесса', 'статус', 'продукт'},
        TableSourceEnum.PAYMENT_PROCESSING: {'наименование процесса', 'статус'},
    }
    
    # Сначала проверяем по минимальным обязательным колонкам
    for source, min_cols in source_min_required.items():
        if min_cols.issubset(excel_cols_set):
            # Если минимальные колонки есть, проверяем дополнительные признаки
            key_cols = source_key_columns[source]
            matches = len(key_cols.intersection(excel_cols_set))
            # Если есть минимум 3 совпадения из ключевых колонок, это наш источник
            if matches >= 3:
                logger.info(f"Detected source: {source.value} (min required: {min_cols}, key matches: {matches})")
                return source
            # Если минимальные колонки есть, но совпадений меньше 3, всё равно возвращаем (для простых случаев)
            elif matches >= len(min_cols):
                logger.info(f"Detected source: {source.value} (min required match, key matches: {matches})")
                return source
    
    # Если не нашли по минимальным, используем подсчет совпадений
    source_scores = {}
    for source, key_cols in source_key_columns.items():
        matches = len(key_cols.intersection(excel_cols_set))
        total_key = len(key_cols)
        # Считаем процент совпадений
        score = matches / total_key if total_key > 0 else 0
        source_scores[source] = (score, matches, total_key)
    
    # Находим источник с максимальным количеством совпадений
    if source_scores:
        best_source = max(source_scores.items(), key=lambda x: (x[1][1], x[1][0]))
        
        # Если есть хотя бы 3 совпадения или 50%+ совпадений, считаем это правильным источником
        if best_source[1][1] >= 3 or best_source[1][0] >= 0.5:
            return best_source[0]
    
    # Fallback: угадать по уникальным колонкам
    if 'нпп' in excel_cols_set:
        return TableSourceEnum.DEPOSITS_FL
    if 'стойбец' in excel_cols_set or 'стойлец' in excel_cols_set:
        return TableSourceEnum.CREDITS_FL
    if 'дата кв' in excel_cols_set and 'фио' in excel_cols_set and 'дата приемки банк' in excel_cols_set:
        return TableSourceEnum.SAFES_RENTAL
    if 'дата кв' in excel_cols_set and 'фио от банка' in excel_cols_set:
        return TableSourceEnum.SAFES_RENTAL
    
    raise ValueError(f"Cannot detect table source from columns: {excel_columns}")


def normalize_status(status_value) -> Optional[str]:
    """
    Нормализует значение статуса из Excel к стандартным значениям StatusEnum.
    
    Args:
        status_value: значение статуса из Excel (может быть строкой, None, или другим типом)
    
    Returns:
        Нормализованное значение статуса или None
    """
    if status_value is None:
        return None
    
    # Преобразуем в строку и нормализуем
    status_str = str(status_value).strip()
    if not status_str:
        return None
    
    # Приводим к lowercase для сравнения
    status_lower = status_str.lower()
    
    # Маппинг различных вариантов написания на стандартные значения
    status_mapping = {
        # Выполнено
        'выполнено': StatusEnum.COMPLETED.value,
        'выполнен': StatusEnum.COMPLETED.value,
        'done': StatusEnum.COMPLETED.value,
        'completed': StatusEnum.COMPLETED.value,
        
        # Успешно
        'успешно': StatusEnum.SUCCESS.value,
        'успешный': StatusEnum.SUCCESS.value,
        'success': StatusEnum.SUCCESS.value,
        'successful': StatusEnum.SUCCESS.value,
        
        # В работе
        'в работе': StatusEnum.IN_PROGRESS.value,
        'в процессе': StatusEnum.IN_PROGRESS.value,
        'выполняется': StatusEnum.IN_PROGRESS.value,
        'in progress': StatusEnum.IN_PROGRESS.value,
        'in_progress': StatusEnum.IN_PROGRESS.value,
        'working': StatusEnum.IN_PROGRESS.value,
        
        # Не начато
        'не начато': StatusEnum.NOT_STARTED.value,
        'не начат': StatusEnum.NOT_STARTED.value,
        'не начата': StatusEnum.NOT_STARTED.value,
        'not started': StatusEnum.NOT_STARTED.value,
        'not_started': StatusEnum.NOT_STARTED.value,
        'pending': StatusEnum.NOT_STARTED.value,
        
        # Не успешно
        'не успешно': StatusEnum.FAILED.value,
        'не успешен': StatusEnum.FAILED.value,
        'не успешна': StatusEnum.FAILED.value,
        'failed': StatusEnum.FAILED.value,
        'failure': StatusEnum.FAILED.value,
        'error': StatusEnum.FAILED.value,
        'ошибка': StatusEnum.FAILED.value,
    }
    
    # Проверяем точное совпадение
    if status_lower in status_mapping:
        normalized = status_mapping[status_lower]
        if status_str != normalized:
            print(f"Status normalized: '{status_str}' -> '{normalized}'")
        return normalized
    
    # Проверяем, может быть это уже стандартное значение (с учетом регистра)
    valid_statuses = [e.value for e in StatusEnum]
    if status_str in valid_statuses:
        return status_str
    
    # Если не нашли точное совпадение, пробуем частичное совпадение
    for key, value in status_mapping.items():
        if key in status_lower or status_lower in key:
            print(f"Status normalized (partial match): '{status_str}' -> '{value}'")
            return value
    
    # Если ничего не подошло, логируем и возвращаем None (валидация потом покажет ошибку)
    print(f"Warning: Could not normalize status value: '{status_str}'")
    return None


def parse_russian_date(date_str: str) -> Optional[str]:
    """
    Парсит русские форматы дат, например: "29 окт. 2025 г."
    """
    if not date_str:
        return None
    
    # Убираем лишние символы
    date_str = date_str.strip().replace('\xa0', ' ').strip()
    
    # Русские названия месяцев
    months_ru = {
        'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'май': 5, 'мая': 5,
        'июн': 6, 'июл': 7, 'авг': 8, 'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12
    }
    
    # Пробуем распарсить формат "29 окт. 2025 г."
    import re
    pattern = r'(\d{1,2})\s+([а-яё]+)\.?\s+(\d{4})\s*г\.?'
    match = re.match(pattern, date_str, re.IGNORECASE)
    if match:
        day = int(match.group(1))
        month_name = match.group(2).lower()[:3]  # первые 3 буквы
        year = int(match.group(3))
        
        if month_name in months_ru:
            month = months_ru[month_name]
            try:
                from datetime import date
                d = date(year, month, day)
                return d.strftime('%Y-%m-%d')
            except ValueError:
                pass
    
    return None


def parse_date(date_value) -> Optional[str]:
    """
    Парсит дату из различных форматов.
    Возвращает строку в формате YYYY-MM-DD для БД или None.
    """
    if date_value is None:
        return None
    
    # Если уже datetime объект
    if isinstance(date_value, datetime):
        return date_value.strftime('%Y-%m-%d')
    
    if isinstance(date_value, str):
        date_str = date_value.strip()
        if not date_str:
            return None
        
        # Пробуем различные форматы (MM/DD/YYYY в начале для американского формата)
        formats = [
            '%m/%d/%Y',      # 11/20/2025 (MM/DD/YYYY - американский формат из Excel)
            '%m/%d/%y',      # 11/20/25
            '%d/%m/%y',      # 20/11/25
            '%d.%m.%y',      # 20.11.25
            '%d/%m/%Y',      # 20/11/2025
            '%d.%m.%Y',      # 20.11.2025
            '%Y-%m-%d',      # 2025-11-20
            '%d/%m/%y %H:%M',  # с временем
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # Пробуем парсить русские форматы дат
        russian_date = parse_russian_date(date_str)
        if russian_date:
            return russian_date
        
        # Если не получилось распарсить, пробуем через dateutil
        try:
            from dateutil import parser
            dt = parser.parse(date_str)
            return dt.strftime('%Y-%m-%d')
        except:
            pass
    
    return None


def map_excel_row_to_record(row_data: dict, source: TableSourceEnum, excel_headers: list) -> dict:
    """
    Маппирует данные из Excel строки в структуру ProcessRecord.
    
    Args:
        row_data: dict с исходными данными из Excel (ключи - нормализованные названия колонок)
        source: определённый источник таблицы
        excel_headers: оригинальные заголовки Excel для маппинга
    
    Returns:
        dict готовый для создания ProcessRecord
    """
    mapping = COLUMN_MAPPINGS[source]
    result = {
        'table_source': source.value,
    }
    
    # Создаём словарь нормализованных заголовков -> оригинальные значения
    normalized_to_original = {}
    for orig_header in excel_headers:
        if orig_header:
            normalized = normalize_column_name(orig_header)
            normalized_to_original[normalized] = orig_header
    
    # Маппирование каждого поля
    # Сначала создаём обратный маппинг: db_field -> список возможных нормализованных названий
    db_field_to_excel_cols = {}
    for excel_col_normalized, db_field in mapping.items():
        if db_field not in db_field_to_excel_cols:
            db_field_to_excel_cols[db_field] = []
        db_field_to_excel_cols[db_field].append(excel_col_normalized)
    
    # Маппируем каждое поле БД
    for db_field, possible_excel_cols in db_field_to_excel_cols.items():
        value = None
        
        # Пробуем найти значение по любому из возможных названий колонок
        for excel_col_normalized in possible_excel_cols:
            if value is not None:
                break
                
            # Ищем в оригинальных заголовках по нормализованному ключу
            for orig_header, orig_value in row_data.items():
                if orig_header:
                    orig_normalized = normalize_column_name(str(orig_header))
                    if orig_normalized == excel_col_normalized:
                        # Для статуса принимаем даже пустые значения (они будут обработаны позже)
                        if db_field == 'status':
                            value = orig_value  # Может быть None или пустая строка
                            break
                        # Для остальных полей проверяем, что значение не пустое
                        elif orig_value is not None:
                            # Для строк проверяем, что не пустая строка
                            if isinstance(orig_value, str):
                                if orig_value.strip():
                                    value = orig_value
                                    break
                            else:
                                value = orig_value
                                break
        
        # Парсинг и обработка значения
        if value is not None:
            if 'date' in db_field:
                value = parse_date(value)
            elif db_field == 'process_number':
                # Парсинг числа
                try:
                    if isinstance(value, str):
                        value = int(re.sub(r'[^\d]', '', value)) if value.strip() else None
                    else:
                        value = int(value) if value else None
                except (ValueError, TypeError):
                    value = None
            elif db_field == 'status':
                # Нормализация статуса
                original_value = value
                value = normalize_status(value)
                # Если статус пустой, устанавливаем значение по умолчанию "Не начато"
                if value is None:
                    if original_value is None or (isinstance(original_value, str) and not original_value.strip()):
                        # Пустой статус - устанавливаем по умолчанию
                        value = StatusEnum.NOT_STARTED.value
                        print(f"Row: Empty status, setting default to '{value}'")
                    else:
                        print(f"Warning: Status could not be normalized. Original value: {repr(original_value)}, type: {type(original_value)}")
                        # Если не удалось нормализовать, устанавливаем по умолчанию
                        value = StatusEnum.NOT_STARTED.value
            elif isinstance(value, str):
                # Очистка строковых значений
                # Убираем невидимые символы (\xa0 - неразрывный пробел и т.д.)
                value = value.replace('\xa0', ' ').strip()
                value = value if value else None
        
        # Особая обработка для статуса - если не найден, устанавливаем по умолчанию
        if db_field == 'status' and value is None:
            print(f"  WARNING: Status field not found in row_data, setting default")
            value = StatusEnum.NOT_STARTED.value
        
        result[db_field] = value
    
    # Логируем результат маппинга для отладки (только если есть проблемы)
    if result.get('status') is None:
        print(f"MAPPED RESULT (with issues):")
        for key, val in result.items():
            print(f"  {key}: {repr(val)}")
    
    return result

