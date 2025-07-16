from src.graphs.intent_routed_qa_graph import build_intent_routed_rag_chain
from src.router.intent_classifier import classify_intent
from langchain_core.messages import HumanMessage, AIMessage

# Initialize chain
rag_chain = build_intent_routed_rag_chain()

# Chat history buffer
chat_history = []

# -------- Query 1 --------
query1 = "Give me all the details about Chandra Prakash?"

# Step 1: Classify intent
intent1 = classify_intent(query1)
print(f"\n🧭 Classified Intent: {intent1}")

# Step 2: RAG chain
response1 = rag_chain.invoke({
    "input": query1,
    "intent": intent1,
    "chat_history": chat_history
})

# Output response
print(f"\n🧠 Query 1: {query1}")
print("📤 Answer:", response1)

# Update history
chat_history.append(HumanMessage(content=query1))
chat_history.append(AIMessage(content=response1))

# -------- Query 2 (Follow-up) --------
query2 = "What subjects does he teach?"

# Step 1: Classify intent
intent2 = classify_intent(query2)
print(f"\n🧭 Classified Intent: {intent2}")

# Step 2: RAG chain
response2 = rag_chain.invoke({
    "input": query2,
    "intent": intent2,
    "chat_history": chat_history
})

# Output response
print(f"\n🧠 Query 2: {query2}")
print("📤 Answer:", response2)

# Update history
chat_history.append(HumanMessage(content=query2))
chat_history.append(AIMessage(content=response2))
