from sqlalchemy import Column, String, Date, Text, Boolean, DateTime, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.database import Base


class ProcessRecord(Base):
    __tablename__ = "process_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Основные данные процесса
    process_name = Column(String(255), nullable=False)
    product_type = Column(String(100), nullable=True)
    status = Column(
        String(50),
        nullable=False,
        index=True
    )

    # Даты и лица
    date_kb = Column(Date, nullable=True)
    fio_customer = Column(String(255), nullable=True)
    date_bank_receipt = Column(Date, nullable=True)
    fio_bank_officer = Column(String(255), nullable=True)

    # Доп. поля
    process_number = Column(Integer, nullable=True)
    bank_employee_name = Column(String(255), nullable=True)
    comments = Column(Text, nullable=True)

    # Служебные
    table_source = Column(String(100), nullable=False, index=True)
    import_date = Column(DateTime, default=datetime.utcnow)
    import_batch_id = Column(String(100), nullable=True, index=True)
    is_archived = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint(
            "status IN ('Выполнено', 'Успешно', 'В работе', 'Не начато', 'Не успешно')",
            name="check_status"
        ),
        # Убрали CheckConstraint для table_source, чтобы можно было создавать динамические чек-листы
    )

