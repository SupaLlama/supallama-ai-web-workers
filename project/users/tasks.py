from celery import shared_task

"""Define as shared_task instead of celery.task 
   to avoid circular imports, and allow this 
   file to work as expected anywhere in the app."""


@shared_task
def divide(x, y):
    # Debugging with rdb
    #
    # from celery.contrib import rdb
    # rdb.set_trace()

    import time
    time.sleep(5)
    return x / y


@shared_task()
def sample_task(email):
    from project.users.views import api_call

    api_call(email)
