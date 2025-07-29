"""LLM-based parser using LangChain and LangGraph."""
from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langgraph.graph import StateGraph, END


class ScheduleAgent:
    """Agent that extracts upcoming openings from raw text."""

    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        llm = ChatOpenAI(model=model, temperature=0)
        prompt = (
            "You are a helpful assistant that extracts available lesson times from text.\n"
            "Return a JSON list of ISO8601 datetimes that represent openings."
        )
        self.chain = create_react_agent(llm, [] , prompt)
        sg = StateGraph(dict)
        sg.add_state("run", self.chain.invoke)
        sg.set_entry_point("run")
        sg.add_edge("run", END)
        self.graph = sg.compile()

    def __call__(self, text: str) -> list[str]:
        result = self.graph.invoke(text)
        return result
