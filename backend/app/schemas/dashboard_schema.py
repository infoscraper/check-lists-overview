from pydantic import BaseModel
from typing import Dict


class SourceSummary(BaseModel):
    total: int
    completed: int
    in_progress: int
    not_started: int


class DashboardSummary(BaseModel):
    total_records: int
    completed: int
    in_progress: int
    not_started: int
    progress_percent: float
    by_source: Dict[str, SourceSummary]

