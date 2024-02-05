import time
# Local Imports
from app.core.celery import celery

@celery.task(name="app.core.tasks.delay_task")
def delay_task():
    """
        Simulate a delay task.

        Returns:
        - A string indicating the task is complete.
    """
    time.sleep(5)
    return "Task Complete"