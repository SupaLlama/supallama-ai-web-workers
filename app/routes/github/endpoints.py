import logging

import requests

from celery.result import AsyncResult

from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse

from . import github_router
from .schemas import CreateReposFromTemplatesBody
from .tasks import create_repos_from_templates_task

@github_router.post("/create-repos-from-templates")
def create_repos_from_templates(request_body: CreateReposFromTemplatesBody):
    task = create_repos_from_templates_task.delay(
        request_body.app_prefix, request_body.repo_template_urls
    )
    return JSONResponse({"task_id": task.task_id})
