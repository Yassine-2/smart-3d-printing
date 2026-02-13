from fastapi import FastAPI
from app.api.printers import router as printer_router
from app.api.jobs import router as jobs_router
import app.events.subscribers

app = FastAPI(
    title="Smart 3D Printing Backend",
    version="0.2.0"
)

app.include_router(printer_router, prefix="/api/printers", tags=["Printers"])
app.include_router(jobs_router, prefix="/api/jobs", tags=["Print Jobs"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

