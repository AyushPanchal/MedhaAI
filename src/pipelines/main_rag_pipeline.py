from src.graphs.intent_routed_qa_graph import build_intent_routed_rag_chain
from src.router.intent_classifier import classify_intent
from src.utils.summarizer import summarize_chat_history
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages.utils import count_tokens_approximately




# Load the graph once
rag_chain = build_intent_routed_rag_chain()

# Max token limit before summarizing
MAX_TOKENS = 10000

# Pipeline entrypoint function
def run_medha_query(query: str, chat_history: list, max_turns: int = 4) -> dict:
    # Recent turns only (e.g. last 2 user+assistant pairs)
    recent_history = chat_history[-2 * max_turns:] if max_turns else []

    # Summarize history if token count exceeds threshold
    memory = ""
    token_count = sum(count_tokens_approximately(msg.content) for msg in chat_history)
    if token_count > MAX_TOKENS:
        print("🧠 Token limit exceeded, summarizing chat history...")
        memory = summarize_chat_history(chat_history)
        print("📝 Summary memory:", memory)

    # Step 1: Classify intent
    intent = classify_intent(query)

    # Step 2: Run graph with input + memory + recent history
    response = rag_chain.invoke({
        "input": query,
        "intent": intent,
        "chat_history": recent_history,
        "memory": memory  # You must support this in your graph
    })

    # Update chat history
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response))

    return {
        "intent": intent,
        "answer": response,
        "chat_history": chat_history
    }
