from celery import shared_task

"""Define as shared_task instead of celery.task 
   to avoid circular imports, and allow this 
   file to work as expected anywhere in the app."""


@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y