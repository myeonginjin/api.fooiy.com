from __future__ import absolute_import

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fooiy.settings")
app = Celery("fooiy")
app.config_from_object("fooiy.celeryconfig")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


@app.task
def debug_add_task(x, y):
    print("result ==>", x + y)
