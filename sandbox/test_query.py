from src.graphs.qa_graph import build_custom_conversational_rag_chain
from langchain_core.messages import HumanMessage, AIMessage

# Initialize the chain
rag_chain = build_custom_conversational_rag_chain()

# Chat memory
chat_history = []

# ✅ Helper function to print result and sources
def print_response(query, response, label=""):
    print(f"\n🧠 {label} {query.strip()}")
    answer = response.get("answer", response) if isinstance(response, dict) else response
    print("📤 Answer:", answer)

    # ✅ Print sources from response
    if isinstance(response, dict) and "sources" in response:
        print("\n📚 Sources:")
        for i, src in enumerate(response["sources"]):
            print(f"🔹 {i + 1}. {src}")


# First question
query1 = "List out all the names of the professors available in the computer department"
res1 = rag_chain.invoke({"input": query1, "chat_history": chat_history})
print_response(query1, res1, "Q1:")
chat_history.append(HumanMessage(content=query1))
chat_history.append(AIMessage(content=res1.get("answer", "") if isinstance(res1, dict) else res1))

# Follow-up
query2 = "list out all the male professors"
res2 = rag_chain.invoke({"input": query2, "chat_history": chat_history})
print_response(query2, res2, "Q2:")
chat_history.append(HumanMessage(content=query2))
chat_history.append(AIMessage(content=res2.get("answer", "") if isinstance(res2, dict) else res2))
