from datetime import datetime

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
