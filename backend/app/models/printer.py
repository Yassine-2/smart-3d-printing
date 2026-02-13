from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrinterCreate(BaseModel):
    name: str
    location: Optional[str] = None

class Printer(BaseModel):
    id: int
    name: str
    location: Optional[str]
    status: str
    created_at: datetime
