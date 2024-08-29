from pydantic import BaseModel

class CreateReposFromTemplatesBody(BaseModel):

    access_token: str
    app_name: str
    app_type: str
    github_username_for_transfer: str