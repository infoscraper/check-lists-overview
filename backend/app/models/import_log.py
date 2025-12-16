from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from app.db.database import Base


class ImportLog(Base):
    __tablename__ = "import_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    import_batch_id = Column(String(100), nullable=False, unique=True, index=True)
    filename = Column(String(255), nullable=True)
    table_source = Column(String(100), nullable=True)
    total_rows = Column(Integer, default=0)
    success_rows = Column(Integer, default=0)
    error_rows = Column(Integer, default=0)
    error_details = Column(JSONB, nullable=True)
    imported_at = Column(DateTime, default=datetime.utcnow)
    imported_by = Column(String(255), nullable=True)

