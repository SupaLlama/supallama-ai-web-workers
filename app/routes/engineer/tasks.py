from celery import shared_task

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import AzureChatOpenAI

from app.config import settings

openai_gpt_4o_model = AzureChatOpenAI(  
    azure_deployment="gpt-4o",  
    api_version="2024-08-01-preview",  
    temperature=0,  
)

tavily_search_tool = TavilySearchResults(
    max_results=5,
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    search_depth="advanced",
)

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
    """LangGraph agentic flow to create web content based on the content description, and optionally other criteria"""

    # Uncomment the 2 lines below to debug
    # this celery task via rdb over telnet!
    #
    # from celery.contrib import rdb
    # rdb.set_trace()

    print(f"Received request to generate code to do the following:\n\n{content_description}\n\n")
