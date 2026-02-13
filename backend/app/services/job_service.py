from datetime import datetime
from typing import List, Optional
from app.events.event_manager import event_manager

# In-memory storage (later replaced by DB)
PRINT_JOBS: List[dict] = []
JOB_ID_SEQ = 1


def create_job(printer_id: int, file_name: str, user_email: Optional[str]):
    global JOB_ID_SEQ

    job = {
        "id": JOB_ID_SEQ,
        "printer_id": printer_id,
        "file_name": file_name,
        "status": "printing",
        "progress": 0.0,
        "created_at": datetime.utcnow(),
        "finished_at": None,
        "user_email": user_email,
    }

    PRINT_JOBS.append(job)
    JOB_ID_SEQ += 1

    # 🔔 Emit job_created event (AI will start here)
    event_manager.emit("job_created", job=job)

    return job


def update_progress(job_id: int, progress: float):
    for job in PRINT_JOBS:
        if job["id"] == job_id:
            job["progress"] = progress

            if progress >= 100:
                job["status"] = "completed"
                job["finished_at"] = datetime.utcnow()

                # 🔔 Emit job_finished event
                event_manager.emit("job_finished", job=job)

            return job

    return None


def fail_job(job_id: int):
    for job in PRINT_JOBS:
        if job["id"] == job_id:
            job["status"] = "failed"
            job["finished_at"] = datetime.utcnow()

            # 🔔 Emit job_failed event
            event_manager.emit("job_failed", job=job)

            return job

    return None


def list_jobs():
    return PRINT_JOBS


def get_job(job_id: int):
    for job in PRINT_JOBS:
        if job["id"] == job_id:
            return job
    return None
