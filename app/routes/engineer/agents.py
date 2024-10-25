import logging

from langchain_core.messages import SystemMessage, ToolMessage

from langgraph.graph import StateGraph, END

from .states import CreateWebContentAgentState


# Logging Config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CreateWebContentAgent") 


# Define a ReAct-like agentic workflow with Reflection
# to create web content based on the user's input
class CreateWebContentAgent:
    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system

        graph = StateGraph(CreateWebContentAgentState)
        graph.add_node("call_model", self.call_model)
        graph.add_node("call_tool", self.call_tool)
        graph.add_conditional_edges("call_model", self.tool_calls_remain, { True: "call_tool", False: END })
        graph.add_edge("call_tool", "call_model")
        graph.set_entry_point("call_model")
        self.graph = graph.compile(checkpointer=checkpointer)

        self.model = model.bind_tools(tools)

        self.tools = {t.name for t in tools}


    def call_model(self, state: CreateWebContentAgentState):
        logger.info(f"Calling the model ...")

        messages = state["messages"]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)

        logger.info(f"The model said:\n{message.content}")

        return { "messages": [message] }


    def call_tool(self, state: CreateWebContentAgentState):
        tool_calls = state["messages"][-1].tool_calls
        tool_call_results = []

        for t in tool_calls:
            logger.info(f"Calling Tool: {t}")
            logger.info(f"self.tools:\n{self.tools}")

            #tool_call_result = self.tools[t["name"]].invoke(t["args"])
            tool_call_result = self.tools[t['name']].invoke(t['args'])

            logger.info(f"Tool call result:\n{tool_call_result}")

            tool_call_results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(tool_call_result)))
            # tool_call_results.append(
            #     ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(tool_call_result))
            # )

        return { "messages": tool_call_results }


    def tool_calls_remain(self, state: CreateWebContentAgentState):
        logger.info(f"Checking if any tool calls remain ...")

        last_message = state["messages"][-1]
        num_tool_calls = len(last_message.tool_calls)

        logger.info(f"{num_tool_calls} tool calls remaining.")

        return num_tool_calls > 0
