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
LANGCHAIN_APP_TYPE: str = "langchain"
LLAMAINDEX_APP_TYPE: str = "llamaindex"
GRIPTAPE_APP_TYPE: str = "griptape"

@shared_task
def create_repos_from_templates_task(app_name: str, app_type: str, github_username_for_transfer: str):
    # Debugging with rdb
    #
    # from celery.contrib import rdb
    # rdb.set_trace()

    print("********** Inside create repos task! ************")
    print(f"app_name: {app_name}")
    print(f"app_type: {app_type}")
    print(f"github_username_for_transfer: {github_username_for_transfer}")

    if app_type == LANGCHAIN_APP_TYPE:
        backend_template = "supallama-rag-backend-python-fastapi-celery-redis-supabase-langchain-pinecone-template"
        frontend_template = "supallama-rag-frontend-typescript-nextjs-shadcnui-supabase-template"
        infrastructure_template = "supallama-rag-render-template"
    elif app_type == GRIPTAPE_APP_TYPE:
        backend_template = "supallama-rag-backend-python-fastapi-celery-redis-supabase-griptape-pinecone-template"
        frontend_template = "supallama-rag-frontend-typescript-nextjs-shadcnui-supabase-template"
        infrastructure_template = "supallama-rag-render-template"

    template_repos: List[str] = [
        backend_template,
        frontend_template,
        infrastructure_template,        
    ]
    
    new_infrastructure_repo_name = f"{app_name}-render"
    new_frontend_repo_name = f"{app_name}-frontend"
    new_backend_repo_name = f"{app_name}-backend"

    new_user_infrastructure_repo_name = f"{app_name}-{github_username_for_transfer}-render"
    new_user_frontend_repo_name = f"{app_name}-{github_username_for_transfer}-frontend"
    new_user_backend_repo_name = f"{app_name}-{github_username_for_transfer}-backend"


    for template_repo in template_repos:
        # Create a copy of the template repo with SupaLlama as the owner
        print(f"Cloning template repo: {template_repo}")   
        new_repo_name = f"{app_name}-"
        new_user_repo_name = f"{app_name}-{github_username_for_transfer}-"
        if template_repo == infrastructure_template:
            new_repo_name += "render"
            new_user_repo_name += "render"
        elif template_repo == frontend_template:
            new_repo_name += "frontend"
            new_user_repo_name += "frontend"
        elif template_repo == backend_template:
            new_repo_name += "backend"
            new_user_repo_name += "backend"

        print(f"new repo name: {new_repo_name}")

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
        print("repo cloned status code", response.status_code)

        time.sleep(1)

        # If Render repo, create a render.yaml file
        if template_repo == infrastructure_template:
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
    name: {app_name}-redis
    region: oregon
    plan: starter # use a plan with persistence
    maxmemoryPolicy: noeviction # recommended policy for queues
    ipAllowList: [] # only allow internal connections
  - type: web
    runtime: node
    name: {app_name}-web
    region: oregon
    repo: https://github.com/{TEMPLATE_OWNER}/{new_frontend_repo_name}
    buildCommand: "npm install; npm run build" 
    startCommand: "npm run start"
    envVars:
      - key: FASTAPI_URL
        fromService:
          name: {app_name}-worker
          type: web
          envVarKey: RENDER_EXTERNAL_URL
  - type: web
    runtime: python
    name: {app_name}-worker
    region: oregon
    repo: https://github.com/{TEMPLATE_OWNER}/{new_backend_repo_name}
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: CELERY_BROKER_URL
        fromService:
          name: {app_name}-redis
          type: redis
          property: connectionString
      - key: CELERY_RESULT_URL
        fromService:
          name: {app_name}-redis
          type: redis
          property: connectionString""".encode("ascii")).decode("ascii")
            }
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            response = requests.put(url, headers=headers, json=data)
            print("writer render.yaml status code", response.status_code)

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
<a href="https://render.com/deploy?repo=https://github.com/{TEMPLATE_OWNER}/{new_infrastructure_repo_name}">
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
            print("write render README status code", response.status_code)


        # Create a 2nd copy of the template repo and transfer ownership to the user
        print(f"Cloning template repo 2nd time: {template_repo}")   
        print(f"New user repo name: {new_user_repo_name}")
        url = f"https://api.github.com/repos/{TEMPLATE_OWNER}/{template_repo}/generate"
        data = { 
            "owner": f"{TEMPLATE_OWNER}",
            "name": new_user_repo_name,
            "private": True
        }
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.post(url, headers=headers, json=data)
        print("2nd copy of repo cloned status code", response.status_code)

        time.sleep(1)

        # If Render repo, create a render.yaml file
        if template_repo == infrastructure_template:
            time.sleep(4)
            print(f"Updating render.yaml file in: {new_user_repo_name}")   
            path = "render.yaml"
            print(f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_user_repo_name}/contents/{path}")
            url = f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_user_repo_name}/contents/{path}"
            data = { 
                "message": "Added render.yaml to define infrastructure blueprint",
                "content": base64.b64encode(
f"""services:
  - type: redis
    name: {app_name}-redis
    region: oregon
    plan: starter # use a plan with persistence
    maxmemoryPolicy: noeviction # recommended policy for queues
    ipAllowList: [] # only allow internal connections
  - type: web
    runtime: node
    name: {app_name}-web
    region: oregon
    repo: https://github.com/{github_username_for_transfer}/{new_user_frontend_repo_name}
    buildCommand: "npm install; npm run build" 
    startCommand: "npm run start"
    envVars:
      - key: FASTAPI_URL
        fromService:
          name: {app_name}-worker
          type: web
          envVarKey: RENDER_EXTERNAL_URL
  - type: web
    runtime: python
    name: {app_name}-worker
    region: oregon
    repo: https://github.com/{github_username_for_transfer}/{new_user_backend_repo_name}
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: CELERY_BROKER_URL
        fromService:
          name: {app_name}-redis
          type: redis
          property: connectionString
      - key: CELERY_RESULT_URL
        fromService:
          name: {app_name}-redis
          type: redis
          property: connectionString""".encode("ascii")).decode("ascii")
            }
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            response = requests.put(url, headers=headers, json=data)
            print("wrote 2nd copy of render.yaml status code", response.status_code)

            path = "README.md"
            print(f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_user_repo_name}/contents/{path}")
            url = f" https://api.github.com/repos/{TEMPLATE_OWNER}/{new_user_repo_name}/contents/{path}"
            data = {
                "message": "Added README file with Deploy button",
                "content": base64.b64encode(
f"""
Click the button below to deploy this app on Render!
<br />
<br />
<a href="https://render.com/deploy?repo=https://github.com/{github_username_for_transfer}/{new_user_infrastructure_repo_name}">
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
            print("wrote 2nd copy of render README status code", response.status_code)

        print("Transferring ownership of 2nd copy of repo")
        url = f"https://api.github.com/repos/{TEMPLATE_OWNER}/{new_user_repo_name}/transfer"
        data = { 
            "new_owner": github_username_for_transfer,
        }
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {settings.GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.post(url, headers=headers, json=data)
        print("repo transfer status code", response.status_code)

        time.sleep(1)
