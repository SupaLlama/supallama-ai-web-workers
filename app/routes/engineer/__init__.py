from fastapi import APIRouter


engineer_router = APIRouter(
    prefix="/engineer"
)


# Import items at the end because endpoints.py
# imports engineer_router from this module init
from . import endpoints, schemas, tasks # noqa
