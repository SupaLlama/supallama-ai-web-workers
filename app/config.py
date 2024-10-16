import os
import pathlib
from functools import lru_cache

"""FastAPI Config"""

class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_URL", "redis://127.0.0.1:6379/0")

    GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN: str = os.environ.get("GITHUB_CLASSIC_PERSONAL_ACCESS_TOKEN", "") 
    GITHUB_PERSONAL_ACCESS_TOKEN: str = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")

    SUPABASE_JWT_SECRET: str = os.environ.get("SUPABASE_JWT_SECRET", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
    MODAL_TOKEN_ID: str = os.environ.get("MODAL_TOKEN_ID", "")
    MODAL_TOKEN_SECRET: str = os.environ.get("MODAL_TOKEN_SECRET", "")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FAST_API_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()