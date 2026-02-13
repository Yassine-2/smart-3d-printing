from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.printers import router as printer_router
from app.api.jobs import router as jobs_router
from app.api.auth import router as auth_router
from app.api.camera import router as camera_router
import app.events.subscribers

app = FastAPI(
    title="Smart 3D Printing Backend",
    version="0.2.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For prototype, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(printer_router, prefix="/api/printers", tags=["Printers"])
app.include_router(jobs_router, prefix="/api/jobs", tags=["Print Jobs"])
app.include_router(camera_router, prefix="/api/camera", tags=["Camera"])

# Serve frontend static files
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")

@app.get("/health")
def health_check():
    return {"status": "ok"}

