from pydantic import BaseModel


class CreateWebContentRequestBody(BaseModel):

    color_scheme: str
    css_library: str
    content_description: str
    next_js_version: str 
    react_control_library: str
    success_criteria: str
    visual_theme: str