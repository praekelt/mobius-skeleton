from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


class DummyScheduler(Scheduler):
    """A scheduler that does nothing."""

    def __init__(self, *args, **kwargs):
        super(DummyScheduler, self).__init__(*args, **kwargs)
        self.schedule = {}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
