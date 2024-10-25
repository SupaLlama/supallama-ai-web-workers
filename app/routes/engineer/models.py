from langchain_openai import AzureChatOpenAI


azure_openai_gpt_4o_model = AzureChatOpenAI(  
    azure_deployment="gpt-4o",  
    api_version="2024-08-01-preview",  
    temperature=0,  
)
