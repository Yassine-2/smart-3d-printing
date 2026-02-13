from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrintJobCreate(BaseModel):
    printer_id: int
    file_name: str
    user_email: Optional[str] = None

class PrintJob(BaseModel):
    id: int
    printer_id: int
    file_name: str
    status: str         # idle / printing / completed / failed
    progress: float     # 0.0 to 100.0
    created_at: datetime
    finished_at: Optional[datetime] = None
    user_email: Optional[str] = None
