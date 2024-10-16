from fastapi import APIRouter

modal_router = APIRouter(
    prefix="/modal",
)

from . import endpoints, schemas, tasks # noqa
