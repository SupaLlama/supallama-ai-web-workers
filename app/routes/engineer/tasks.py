import logging

from celery import shared_task

from langchain_core.messages import HumanMessage

from langgraph.checkpoint.memory import MemorySaver

from .agents import CreateWebContentAgent
from .models import azure_openai_gpt_4o_model
from .prompts import engineer_system_prompt_template
from .schemas import ChatMessage
from .states import CreateWebContentAgentState
from .tools import tavily_search_tool


# Logging Config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("engineer-tasks") 


@shared_task # use @shared_task to avoid circular imports
def create_web_content_agentic_task(
    content_description: str, 
    color_scheme: str = "Use a largely white and black color scheme with some shades of gray to brighten things up", 
    css_framework: str = "Use the Tailwind CSS framework when generating code", 
    next_js_version: str = "Ensure that the generated code is a React page component that's compatible with Next.js version 14 and the App Router",
    react_control_library: str = "Use the shadcn UI react component library for controls, graphs, charts and visualizations",
    success_criteria: str = "Use common sense to determine whether the generated code matches the request", 
    visual_theme: str = "Minimalist, artistic, clean theme",
    ) -> str:
    """LangGraph agentic flow to create web content based on 
    the content description, and optionally other criteria"""

    # Uncomment the 2 lines below to debug
    # this celery task via rdb over telnet!
    #
    # from celery.contrib import rdb
    # rdb.set_trace()

    logger.info(f"Received request to generate code to do the following:\n{content_description}")

    try:
        create_web_content_system_prompt = engineer_system_prompt_template.format(
            color_scheme=color_scheme,
            css_framework=css_framework,
            next_js_version=next_js_version,
            react_control_library=react_control_library,
            success_criteria=success_criteria,
            visual_theme=visual_theme
        )

        # Create an instance of the agent to import in tasks
        create_web_content_agent = CreateWebContentAgent(
            model=azure_openai_gpt_4o_model,
            tools=[tavily_search_tool],
            checkpointer=MemorySaver(),
            system=create_web_content_system_prompt
        )

        messages = [HumanMessage(content=content_description)]

        thread_id = "1"
        thread_config = {"configurable": {"thread_id": thread_id}}

        response = create_web_content_agent.graph.invoke(input={"messages": messages}, config=thread_config)
        output = response["messages"][-1]
    
        logger.info(f"Received the following output from the create_web_content_agent:\n{output.content}")
    
    except Exception as e:
        logger.error(f"Exception in create_web_content_agentic_task: {e}")
