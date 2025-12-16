from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.dashboard_schema import DashboardSummary, SourceSummary
from app.services.record_service import get_dashboard_summary

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_summary(db: Session = Depends(get_db)):
    """Получить сводку для dashboard"""
    summary_data = get_dashboard_summary(db)
    
    # Преобразуем by_source в SourceSummary объекты
    by_source = {
        source: SourceSummary(**data)
        for source, data in summary_data['by_source'].items()
    }
    
    return DashboardSummary(
        total_records=summary_data['total_records'],
        completed=summary_data['completed'],
        in_progress=summary_data['in_progress'],
        not_started=summary_data['not_started'],
        progress_percent=summary_data['progress_percent'],
        by_source=by_source
    )

