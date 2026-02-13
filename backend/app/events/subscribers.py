import threading
from app.events.event_manager import event_manager
from app.events.ai_monitor import monitor_printer


# -------------------------
# LOGGING (debug / visibility)
# -------------------------
def log_job_event(job, **kwargs):
    """Log job events. Accepts kwargs for compatibility with error events."""
    status = job.get('status', 'unknown')
    print(f"[EVENT] Job {job['id']} → {status}")
    if 'error' in kwargs:
        print(f"[EVENT] Error details: {kwargs['error']}")


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
    """Start AI monitoring thread with error handling."""
    print(f"[AI] Starting monitor for job {job['id']}")

    def monitor_with_error_handling():
        """Wrapper to catch and log any errors during monitoring startup."""
        try:
            monitor_printer(job)
        except Exception as e:
            error_msg = f"Failed to start AI monitor for job {job['id']}: {str(e)}"
            print(f"[AI] ERROR: {error_msg}")
            # Emit error event if monitoring fails to start
            event_manager.emit("job_monitoring_failed", job=job, error=error_msg)

    t = threading.Thread(
        target=monitor_with_error_handling,
        daemon=True
    )
    t.start()


# -------------------------
# SUBSCRIPTIONS
# -------------------------
event_manager.subscribe("job_created", start_ai_monitor)

event_manager.subscribe("job_finished", log_job_event)
event_manager.subscribe("job_failed", log_job_event)
event_manager.subscribe("job_monitoring_failed", log_job_event)

event_manager.subscribe("job_finished", notify_user)
event_manager.subscribe("job_failed", notify_user)
