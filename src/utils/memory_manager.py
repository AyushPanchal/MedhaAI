# src/utils/memory_manager.py
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.utils.token_length import get_token_length
from src.utils.summarizer import summarize_chat_history

MAX_TOKEN_LIMIT = 12000  # Stay well under 16k limit
SUMMARY_PREFIX = "Memory Summary:"

def get_recent_messages(chat_history, max_tokens=MAX_TOKEN_LIMIT):
    total_tokens = sum(get_token_length(m.content) for m in chat_history)

    if total_tokens <= max_tokens:
        return chat_history

    # Summarize and truncate older history
    summary = summarize_chat_history(chat_history)
    return [HumanMessage(content=SUMMARY_PREFIX), AIMessage(content=summary)]

def update_memory(chat_history, user_input, ai_response):
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=ai_response))
