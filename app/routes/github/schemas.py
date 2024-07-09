from pydantic import BaseModel
from typing import List

class CreateReposFromTemplatesBody(BaseModel):

    app_prefix: str
    repo_template_urls: List[str]
