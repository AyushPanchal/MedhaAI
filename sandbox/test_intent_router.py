from src.router.intent_router import route_query
from langchain_core.messages import HumanMessage, AIMessage

chat_history = []

query1 = "Who is HoD?"
res1 = route_query(query1, chat_history)
print("Q1:", query1)
print("A1:", res1)

chat_history.append(HumanMessage(content=query1))
chat_history.append(AIMessage(content=res1 if isinstance(res1, str) else res1.get("answer", "")))
