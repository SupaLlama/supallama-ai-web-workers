import logging

from fastapi.responses import JSONResponse

from app.jwt_utils import verify_jwt
from app.supabase_utils import get_user_from_supabase_auth

from . import github_router
from .schemas import CreateReposFromTemplatesBody
from .tasks import create_repos_from_templates_task

# Logging Config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("github-endpoints") 


@github_router.post("/create-repos-from-templates")
def create_repos_from_templates(request_body: CreateReposFromTemplatesBody) -> JSONResponse:
    """
    If the user's access token is valid, then queue
    a background worker to generate the one or more
    GitHub repositories in the specified template 
    """
    logger.info("In '/create_repos_from_templates' route handler")

    logger.info("Validating the reqeust body parameters")
    if request_body.access_token is None or type(request_body.access_token) is not str:
        logger.error(f"Invalid JWT: {request_body.access_token}")
        return JSONResponse({"error": "Invalid JWT"})

    if request_body.app_name is None or type(request_body.app_name) is not str:
        logger.error(f"Invalid App Name: {request_body.app_name}")
        return JSONResponse({"error": "Invalid App Name"})

    if request_body.app_type is None or type(request_body.app_type) is not str:
        logger.error(f"Invalid App Type: {request_body.app_type}")
        return JSONResponse({"error": "Invalid App Type"})

    logger.info("Verifying the JWT using the JWT Secret and 'authenticated' audience")
    if not verify_jwt(request_body.access_token, 'authenticated'):
        logger.error(f"Unable to verify JWT: {request_body.access_token}")
        return JSONResponse({"error": "Unable to verify JWT"})

    logger.info("Getting the user from the Supabase Auth database to ensure that JWT is up-to-date")
    user_id = get_user_from_supabase_auth(request_body.access_token)

    logger.info("Verifying the JWT using the JWT Secret and 'authenticated' audience")
    task = create_repos_from_templates_task.delay(
        user_id,
        request_body.app_name,
        request_body.app_type,
        request_body.github_username_for_transfer,
    )
    return JSONResponse({"task_id": task.task_id})
