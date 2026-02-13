from fastapi import APIRouter
from app.models.printer import PrinterCreate, Printer
from app.services.printer_service import register_printer

router = APIRouter()

@router.post("/register", response_model=Printer)
def register(printer: PrinterCreate):
    return register_printer(
        name=printer.name,
        location=printer.location
    )
