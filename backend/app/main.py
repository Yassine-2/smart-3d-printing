from fastapi import FastAPI
from app.api.printers import router as printer_router

app = FastAPI(
    title="Smart 3D Printing Backend",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# API Routers
app.include_router(printer_router, prefix="/api/printers", tags=["Printers"])
