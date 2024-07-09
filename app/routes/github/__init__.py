from fastapi import APIRouter

github_router = APIRouter(
    prefix="/github",
)

from . import endpoints, schemas, tasks # noqa
