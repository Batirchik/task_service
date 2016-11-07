from cache import c
import time
from celery_app import celery_app


@celery_app.task(name='storing_data_to_file')
def storing_data_to_file():
    """Run task."""
    print ('Task has being started!!!')
    key = 'task_success'
    c.set_data(key, 'foo', 60)
    time.sleep(60)
    c.del_data(key)
    print 'Done!!!'
