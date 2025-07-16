# src/router/intent_router.py

from src.router.intent_classifier import classify_intent
from src.graphs.qa_graph import build_custom_conversational_rag_chain

# 🔁 (Later, import other intent-specific chains like course_syllabus_chain, faculty_details_chain, etc.)

# Instantiate chains once
qa_chain = build_custom_conversational_rag_chain()

# Intent to chain mapping
intent_to_chain = {
    "academic_query": qa_chain,
    "faculty_details": qa_chain,
    "course_syllabus": qa_chain,
    "lab_info": qa_chain,
    "timetable": qa_chain,
    "placement_statistics": qa_chain,
    "contact_info": qa_chain,
    # Add more intent: chain mappings here
}


def route_query(user_input: str, chat_history: list):
    intent = classify_intent(user_input)
    chain = intent_to_chain.get(intent)

    if not chain:
        return f"❌ Sorry, I couldn't route your query to the right department."

    return chain.invoke({"input": user_input, "chat_history": chat_history})
