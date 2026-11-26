from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def research_agent(state):
    results = client.search(query=state["topic"], max_results=5)
    text = "\n\n".join(r["content"] for r in results["results"])
    return {"research": text}