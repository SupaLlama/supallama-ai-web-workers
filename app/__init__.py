from fastapi import FastAPI

from app.celery_utils import create_celery



def create_fastapi_app() -> FastAPI:
    """FastAPI Factory Function"""

    app = FastAPI()

    #  Call Celery Factory function *BEFORE* loading routes
    app.celery_app = create_celery()

    # Load routes
    from app.routes.github import github_router
    app.include_router(github_router)

    from app.routes.engineer import engineer_router
    app.include_router(engineer_router)

    @app.get("/")
    async def root():
        return {"Ping": "Pong"}

    return app
