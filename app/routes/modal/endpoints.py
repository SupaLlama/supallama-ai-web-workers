import logging

from fastapi.responses import JSONResponse

from . import modal_router
from .schemas import TestModalBody
from .tasks import test_modal_task

# Logging Config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("modal-endpoints") 


@modal_router.get("/test-modal")
def test_modal() -> JSONResponse:
    """
    """
    logger.info("In '/test-modal' route handler")
    test_modal_task.delay()
    return JSONResponse({"response_code": 200})
