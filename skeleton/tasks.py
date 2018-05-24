from celery.decorators import periodic_task
from celery.task.schedules import crontab


@periodic_task(
    run_every=crontab(hour="*", minute="*/1"),
    ignore_result=True
)
def sample_task():
    print("Sample task")
