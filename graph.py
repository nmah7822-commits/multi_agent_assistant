from langgraph.graph import StateGraph, START, END
from state import AgentState
from agents.research_agent import research_agent
from agents.report_agent import report_agent

builder = StateGraph(AgentState)
builder.add_node("research", research_agent)
builder.add_node("report", report_agent)

builder.add_edge(START, "research")
builder.add_edge("research", "report")
builder.add_edge("report", END)

graph = builder.compile()