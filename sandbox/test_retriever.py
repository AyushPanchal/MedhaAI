# sandbox/test_retriever.py

from src.retrievers.intent_retriever import get_retriever_for_intent
from dotenv import load_dotenv

load_dotenv()

def test_retriever():
    test_intent = "faculty_details"  # or any other intent you've already indexed
    retriever = get_retriever_for_intent(test_intent)

    test_query = "Who is the Head of Department?"
    docs = retriever.invoke(test_query)

    print(f"\n📚 Retrieved {len(docs)} documents for intent: '{test_intent}'")
    for i, doc in enumerate(docs):
        print(f"\n🔹 Doc {i + 1}")
        print(f"Content: {doc.page_content[:300]}...")
        print(f"Source: {doc.metadata.get('source', 'N/A')}")


if __name__ == "__main__":
    test_retriever()
