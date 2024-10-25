import operator
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage


class CreateWebContentAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
