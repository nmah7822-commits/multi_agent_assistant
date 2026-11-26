from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)

def report_agent(state):
    prompt = f"""You are a business analyst.
Write a short professional report on: {state['topic']}

Use only this research:
{state['research']}

Format: Summary, Key Points, Recommendation."""
    response = llm.invoke(prompt)
    return {"report": response.content}