from src.graphs.intent_routed_qa_graph import build_intent_routed_rag_chain
from src.router.intent_classifier import classify_intent
from langchain_core.messages import HumanMessage, AIMessage

# Load the graph once
rag_chain = build_intent_routed_rag_chain()

# Pipeline entrypoint function
def run_medha_query(query: str, chat_history: list, max_turns: int = 4) -> dict:
    from langchain_core.messages import HumanMessage, AIMessage

    # Slice last `max_turns` (each turn = Human + AI)
    recent_history = chat_history[-2 * max_turns :] if max_turns else []

    # Step 1: Classify intent
    intent = classify_intent(query)

    # Step 2: Run graph
    response = rag_chain.invoke({
        "input": query,
        "intent": intent,
        "chat_history": recent_history
    })

    # Update original history
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response))

    return {
        "intent": intent,
        "answer": response,
        "chat_history": chat_history
    }