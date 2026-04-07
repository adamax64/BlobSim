"""
Scheduler management service for dynamic cronjob control.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from cronjobs.progress_simulation import run_progress_simulation
from cronjobs.progress_competition import progress_competition

_scheduler_instance = None


def get_scheduler() -> AsyncIOScheduler:
    """Get the global scheduler instance."""
    return _scheduler_instance


def start_scheduler():
    """Start the cronjobs scheduler if not already running."""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = AsyncIOScheduler()
        _scheduler_instance.add_job(
            run_progress_simulation, CronTrigger(hour=6, minute=0)
        )  # Run daily at 6 AM
        _scheduler_instance.add_job(
            progress_competition,
            CronTrigger(minute="*/3", hour="12-17"),
        )  # Run every 3 minutes from 12:00 to 17:57

    if not _scheduler_instance.running:
        _scheduler_instance.start()
        print("[INFO] Scheduler started dynamically.")


def stop_scheduler():
    """Stop the cronjobs scheduler if running."""
    global _scheduler_instance
    if _scheduler_instance and _scheduler_instance.running:
        _scheduler_instance.shutdown(wait=False)
        print("[INFO] Scheduler stopped dynamically.")


def is_scheduler_running() -> bool:
    """Check if the scheduler is currently running."""
    return _scheduler_instance is not None and _scheduler_instance.running
