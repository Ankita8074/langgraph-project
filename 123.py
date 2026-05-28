from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.environ.get("OPENAI_API_KEY"))
class AgentState(TypedDict):
    messages: list
    category: str

def classify(state: AgentState):
    user_msg = state["messages"][-1]
    prompt = f"Classify this customer message into one of: order, refund, shipping, general. Message: {user_msg}. Reply with just the category word."
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": state["messages"], "category": result.content.strip().lower()}

def respond(state: AgentState):
    user_msg = state["messages"][-1]
    category = state["category"]
    prompt = f"You are a helpful e-commerce customer support agent. Category: {category}. Customer message: {user_msg}. Give a helpful response."
    result = llm.invoke([HumanMessage(content=prompt)])
    print(f"\nCategory: {category}")
    print(f"Bot: {result.content}")
    return {"messages": state["messages"] + [result.content], "category": category}

workflow = StateGraph(AgentState)
workflow.add_node("classify", classify)
workflow.add_node("respond", respond)
workflow.set_entry_point("classify")
workflow.add_edge("classify", "respond")
workflow.add_edge("respond", END)

app = workflow.compile()

print("E-commerce Customer Support Bot")
print("================================")
questions = [
    "Where is my order #12345?",
    "I want to return my shoes",
    "When will my package arrive?"
]
for q in questions:
    print(f"\nCustomer: {q}")
    app.invoke({"messages": [q], "category": ""})