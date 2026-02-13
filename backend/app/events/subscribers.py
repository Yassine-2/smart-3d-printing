import threading
from app.events.event_manager import event_manager
from app.events.ai_monitor import monitor_printer


# -------------------------
# LOGGING (debug / visibility)
# -------------------------
def log_job_event(job):
    print(f"[EVENT] Job {job['id']} → {job['status']}")


# -------------------------
# EMAIL PLACEHOLDER
# -------------------------
def notify_user(job):
    if job.get("user_email"):
        print(
            f"[EMAIL] To: {job['user_email']} | "
            f"Job {job['id']} status: {job['status']}"
        )


# -------------------------
# AI STARTER
# -------------------------
def start_ai_monitor(job):
    print(f"[AI] Starting monitor for job {job['id']}")

    t = threading.Thread(
        target=monitor_printer,
        args=(job,),
        daemon=True
    )
    t.start()


# -------------------------
# SUBSCRIPTIONS
# -------------------------
event_manager.subscribe("job_created", start_ai_monitor)

event_manager.subscribe("job_finished", log_job_event)
event_manager.subscribe("job_failed", log_job_event)

event_manager.subscribe("job_finished", notify_user)
event_manager.subscribe("job_failed", notify_user)
