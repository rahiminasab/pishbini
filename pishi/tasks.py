from __future__ import absolute_import, unicode_literals

from celery import shared_task

from datetime import timedelta
from celery.task import periodic_task


#@periodic_task(run_every=timedelta(seconds=10), name="calc_scores")
@shared_task()
def calc_scores():
    print 'i am called!!'