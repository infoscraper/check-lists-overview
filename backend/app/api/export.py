from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.excel_exporter import export_to_excel
from typing import Optional
from io import BytesIO

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/excel")
def export_excel_file(
    table_source: Optional[str] = Query(None, description="Фильтр по источнику"),
    db: Session = Depends(get_db)
):
    """
    Экспортирует данные в Excel файл.
    """
    wb = export_to_excel(db, table_source)
    
    # Сохраняем в BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    filename = f"process_records_{table_source or 'all'}.xlsx"
    
    return Response(
        content=output.read(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

