from celery import shared_task

from typing import List

"""Define as shared_task instead of celery.task 
   to avoid circular imports, and allow this 
   file to work as expected anywhere in the app."""


@shared_task
def create_repos_from_templates_task(app_prefix: str, repo_urls: List[str]) -> str:
    # Debugging with rdb
    #
    # from celery.contrib import rdb
    # rdb.set_trace()

    print("********** Inside create repos task! ************")
    print(f"app_prefix: {app_prefix}")
    print(f"repo_urls: {repo_urls}")

    import time
    time.sleep(2)
    return 'forked!'
