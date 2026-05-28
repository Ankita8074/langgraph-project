from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    next: str

def agent_function(state: AgentState):
    print("Agent running...")
    return {"messages": state["messages"], "next": "tool"}

def tool_function(state: AgentState):
    print("Tool running...")
    return {"messages": state["messages"], "next": "end"}

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_function)
workflow.add_node("tool", tool_function)
workflow.set_entry_point("agent")
workflow.add_edge("agent", "tool")
workflow.add_edge("tool", END)

app = workflow.compile()
result = app.invoke({"messages": ["Hello"], "next": ""})
print("Done!", result)