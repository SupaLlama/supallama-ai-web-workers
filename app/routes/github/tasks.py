from celery import shared_task

import requests

from typing import List

from app.config import settings

"""Define as shared_task instead of celery.task 
   to avoid circular imports, and allow this 
   file to work as expected anywhere in the app."""

# Constants
TEMPLATE_OWNER: str = "SupaLlama"
TEMPLATE_REPOS: List[str] = [
    "supallama-worker-starter",
    "supallama-web-starter",
    "supallama-render-starter"
]


@shared_task
def create_repos_from_templates_task(app_prefix: str):
    # Debugging with rdb
    #
    # from celery.contrib import rdb
    # rdb.set_trace()

    print("********** Inside create repos task! ************")
    print(f"app_prefix: {app_prefix}")

    for template_repo in TEMPLATE_REPOS:
        print(f"Cloning template repo: {template_repo}")   

        url = f"https://api.github.com/repos/{TEMPLATE_OWNER}/{template_repo}/generate"
        data = { 
            "owner": f"{TEMPLATE_OWNER}",
            "name": f"{app_prefix}-{template_repo}",
            "private": True
        }
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {settings.GITHUB_PERSONAL_ACCESS_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        response = requests.post(url, headers=headers, json=data)
        print("status code", response.status_code)
