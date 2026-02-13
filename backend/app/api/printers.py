from fastapi import APIRouter, HTTPException
from app.models.printer import PrinterCreate, Printer
from app.services.printer_service import register_printer, list_printers, get_printer

router = APIRouter()

@router.post("/register", response_model=Printer)
def register(printer: PrinterCreate):
    return register_printer(
        name=printer.name,
        location=printer.location
    )

@router.get("/list", response_model=list[Printer])
def api_list_printers():
    return list_printers()

@router.get("/{printer_id}", response_model=Printer)
def api_get_printer(printer_id: int):
    printer = get_printer(printer_id)
    if not printer:
        raise HTTPException(status_code=404, detail="Printer not found")
    return printer
