from fastapi import FastAPI

# from app.celery_utils import create_celery

# from . import tasks


def create_fastapi_app() -> FastAPI:
    """FastAPI Factory Function"""

    app = FastAPI()

    # #  Call Celery Factory function *BEFORE* loading routes
    # app.celery_app = create_celery()

    # # Load routes
    # from app.users import users_router
    # app.include_router(users_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
