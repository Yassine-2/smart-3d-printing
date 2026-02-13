from fastapi import APIRouter, HTTPException
from app.models.job import PrintJobCreate, PrintJob
from app.services.job_service import create_job, update_progress, fail_job, list_jobs

router = APIRouter()

@router.post("/create", response_model=PrintJob)
def api_create_job(job: PrintJobCreate):
    return create_job(
        printer_id=job.printer_id,
        file_name=job.file_name,
        user_email=job.user_email
    )

@router.post("/{job_id}/progress", response_model=PrintJob)
def api_update_progress(job_id: int, progress: float):
    updated = update_progress(job_id, progress)
    if not updated:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated

@router.post("/{job_id}/fail", response_model=PrintJob)
def api_fail_job(job_id: int):
    failed = fail_job(job_id)
    if not failed:
        raise HTTPException(status_code=404, detail="Job not found")
    return failed

@router.get("/list", response_model=list[PrintJob])
def api_list_jobs():
    return list_jobs()
