from fastapi.responses import JSONResponse

from . import engineer_router
from .schemas import CreateWebContentRequestBody
from .tasks import create_web_content_agentic_task

@engineer_router.post("/create-web-content")
def create_web_content(request_body: CreateWebContentRequestBody):
    # Offload the agentic workflow to the background
    celery_task = create_web_content_agentic_task.delay(
        request_body.content_description,
    )

    # Return the Celery Task ID to allow 
    # the UI to check on the task's status.
    return JSONResponse({ "task_id": celery_task.task_id })
