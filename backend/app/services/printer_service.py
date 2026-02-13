from datetime import datetime
from typing import List, Optional

# Temporary in-memory storage (will be replaced by DB)
PRINTERS = []
PRINTER_ID_SEQ = 1

def register_printer(name: str, location: str | None):
    global PRINTER_ID_SEQ

    printer = {
        "id": PRINTER_ID_SEQ,
        "name": name,
        "location": location,
        "status": "idle",
        "created_at": datetime.utcnow()
    }

    PRINTERS.append(printer)
    PRINTER_ID_SEQ += 1

    return printer


def list_printers() -> List[dict]:
    """Return all registered printers."""
    return PRINTERS


def get_printer(printer_id: int) -> Optional[dict]:
    """Get a printer by ID. Returns None if not found."""
    for printer in PRINTERS:
        if printer["id"] == printer_id:
            return printer
    return None
