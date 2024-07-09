from celery import shared_task

import requests

from typing import List

from app.config import settings

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
    
    github_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

    TEMPLATE_OWNER = "SupaLlama"
    TEMPLATE_REPO = "supallama-worker-starter" 

    url = f"https://api.github.com/repos/{TEMPLATE_OWNER}/{TEMPLATE_REPO}/generate"
    print("url", url)
    data = { 
        "owner": "supallama",
        "name": "ash-created-this-repo-from-a-template",
        "private": True
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.post(url, headers=headers, json=data)
    print("status code", response.status_code)
    print("json response", response.json())

    return "created?!"
