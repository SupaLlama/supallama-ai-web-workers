import base64
import time
from typing import List

from celery import shared_task

import requests

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

        # Create a copy of the template repo with SupaLlama as the owner
        print(f"Cloning template repo: {template_repo}")   
        new_repo_name = f"{app_prefix}-supallama-copy-created-via-{template_repo}"
        print(new_repo_name)
        url = f"https://api.github.com/repos/{TEMPLATE_OWNER}/{template_repo}/generate"
        data = { 
            "owner": f"{TEMPLATE_OWNER}",
            "name": new_repo_name,
            "private": True
        }
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.post(url, headers=headers, json=data)
        print("status code", response.status_code)

        time.sleep(1)

        # If Render repo, create a render.yaml file
        if template_repo == "supallama-render-starter":
            time.sleep(4)
            print(f"Updating render.yaml file in: {new_repo_name}")   
            path = "render.yaml"
            print(f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/contents/{path}")
            url = f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/contents/{path}"
            data = { 
                "message": "Added render.yaml to define infrastructure blueprint",
                "content": base64.b64encode(
f"""services:
  - type: redis
    name: {app_prefix}-supallama-copy-created-via-supallama-redis-starter
    region: oregon
    plan: starter # use a plan with persistence
    maxmemoryPolicy: noeviction # recommended policy for queues
    ipAllowList: [] # only allow internal connections
  - type: web
    runtime: node
    name: {app_prefix}-supallama-copy-created-via-supallama-web-starter
    region: oregon
    repo: https://github.com/SupaLlama/{app_prefix}-supallama-copy-created-via-supallama-web-starter
    buildCommand: "npm install; npm run build" 
    startCommand: "npm run start"
    envVars:
      - key: FASTAPI_URL
        fromService:
          name: {app_prefix}-supallama-copy-created-via-supallama-worker-starter
          type: web
          envVarKey: RENDER_EXTERNAL_URL
  - type: web
    runtime: python
    name: {app_prefix}-supallama-copy-created-via-supallama-worker-starter
    region: oregon
    repo: https://github.com/SupaLlama/{app_prefix}-supallama-copy-created-via-supallama-worker-starter
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: CELERY_BROKER_URL
        fromService:
          name: {app_prefix}-supallama-copy-created-via-supallama-redis-starter
          type: redis
          property: connectionString
      - key: CELERY_RESULT_URL
        fromService:
          name: {app_prefix}-supallama-copy-created-via-supallama-redis-starter
          type: redis
          property: connectionString""".encode("ascii")).decode("ascii")
            }
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            response = requests.put(url, headers=headers, json=data)
            print("status code", response.status_code)
            print(response.json())

            path = "README.md"
            print(f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/contents/{path}")
            url = f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/contents/{path}"
            data = {
                "message": "Added README file with Deploy button",
                "content": base64.b64encode(
f"""
Click the button below to deploy this app on Render!
<br />
<br />
<a href="https://render.com/deploy?repo=https://github.com/{TEMPLATE_OWNER}/{app_prefix}-supallama-copy-created-via-supallama-render-starter">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" />
</a>
""".encode("ascii")).decode("ascii")
            } 
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            response = requests.put(url, headers=headers, json=data)
            print("status code", response.status_code)
            print(response.json())

        # Create a 2nd copy of the template repo and transfer ownership to the user
        print(f"Cloning template repo: {template_repo}")   
        new_repo_name = f"{app_prefix}-user-copy-created-via-{template_repo}"
        print(new_repo_name)
        url = f"https://api.github.com/repos/{TEMPLATE_OWNER}/{template_repo}/generate"
        data = { 
            "owner": f"{TEMPLATE_OWNER}",
            "name": new_repo_name,
            "private": True
        }
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.post(url, headers=headers, json=data)
        print("status code", response.status_code)

        time.sleep(1)

        # If Render repo, create a render.yaml file
        if template_repo == "supallama-render-starter":
            time.sleep(4)
            print(f"Updating render.yaml file in: {new_repo_name}")   
            path = "render.yaml"
            print(f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/contents/{path}")
            url = f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/contents/{path}"
            data = { 
                "message": "Added render.yaml to define infrastructure blueprint",
                "content": base64.b64encode(
f"""services:
  - type: redis
    name: {app_prefix}-user-copy-created-via-supallama-redis-starter
    region: oregon
    plan: starter # use a plan with persistence
    maxmemoryPolicy: noeviction # recommended policy for queues
    ipAllowList: [] # only allow internal connections
  - type: web
    runtime: node
    name: {app_prefix}-user-copy-created-via-supallama-web-starter
    region: oregon
    repo: https://github.com/SupaLlama/{app_prefix}-user-copy-created-via-supallama-web-starter
    buildCommand: "npm install; npm run build" 
    startCommand: "npm run start"
    envVars:
      - key: FASTAPI_URL
        fromService:
          name: {app_prefix}-user-copy-created-via-supallama-worker-starter
          type: web
          envVarKey: RENDER_EXTERNAL_URL
  - type: web
    runtime: python
    name: {app_prefix}-user-copy-created-via-supallama-worker-starter
    region: oregon
    repo: https://github.com/SupaLlama/{app_prefix}-user-copy-created-via-supallama-worker-starter
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: CELERY_BROKER_URL
        fromService:
          name: {app_prefix}-user-copy-created-via-supallama-redis-starter
          type: redis
          property: connectionString
      - key: CELERY_RESULT_URL
        fromService:
          name: {app_prefix}-user-copy-created-via-supallama-redis-starter
          type: redis
          property: connectionString""".encode("ascii")).decode("ascii")
            }
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            response = requests.put(url, headers=headers, json=data)
            print("status code", response.status_code)

            path = "README.md"
            print(f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/contents/{path}")
            url = f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/contents/{path}"
            data = {
                "message": "Added README file with Deploy button",
                "content": base64.b64encode(
f"""
Click the button below to deploy this app on Render!
<br />
<br />
<a href="https://render.com/deploy?repo=https://github.com/{TEMPLATE_OWNER}/{app_prefix}-user-copy-created-via-supallama-render-starter">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" />
</a>
""".encode("ascii")).decode("ascii")
            } 
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            response = requests.put(url, headers=headers, json=data)
            print("status code", response.status_code)

        print("Transferring ownership of 2nd copy of repo")
        url = f"https://api.github.com/repos/{TEMPLATE_OWNER}/{new_repo_name}/transfer"
        data = { 
            "new_owner": "ashtable",
        }
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.post(url, headers=headers, json=data)
        print("status code", response.status_code)

        time.sleep(1)
