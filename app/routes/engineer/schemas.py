from typing import Optional

from pydantic import BaseModel


class CreateWebContentRequestBody(BaseModel):

    color_scheme: Optional[str] = None
    css_library: Optional[str] = None
    content_description: str
    next_js_version: Optional[str] = None
    react_control_library: Optional[str] = None
    success_criteria: Optional[str] = None
    visual_theme: Optional[str] = None