from celery import shared_task

import modal

app = modal.App('testing-modal')

@app.function(image=modal.Image.debian_slim().pip_install("celery"))
def square(x):
    print("This code is running on a remote worker!")
    return x**2

"""Define as shared_task instead of celery.task 
   to avoid circular imports, and allow this 
   file to work as expected anywhere in the app."""

@shared_task
def test_modal_task():
    # Debugging with rdb
    #
    # from celery.contrib import rdb
    # rdb.set_trace()
    with app.run():
        print("the square is", square.remote(42))

