# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/01 14:38:08
@Author  :   47bwy
@Desc    :   None
'''

from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def periodic_task():
    return "Running every minute"

app.conf.beat_schedule = {
    'every-minute': {
        'task': 'tasks.periodic_task',
        'schedule': crontab(minute='*/1'),
        'args': ()
    },
}