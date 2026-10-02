from fastapi import BackgroundTasks

# This module can be extended to centralize background work orchestration.

def enqueue(background_tasks: BackgroundTasks, func, *args, **kwargs):
    background_tasks.add_task(func, *args, **kwargs)
