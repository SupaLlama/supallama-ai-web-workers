from langchain_community.tools.tavily_search import TavilySearchResults

tavily_search_tool = TavilySearchResults(
    max_results=5,
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    search_depth="advanced",
)
