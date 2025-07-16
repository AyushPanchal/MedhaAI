import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_BASE_DIR = r"C:\Users\Ayush\OneDrive\Desktop\MedhaAI\faiss_indexes"


def get_retriever_for_intent(intent: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    index_path = os.path.join(INDEX_BASE_DIR, f"{intent}_index")

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found for intent: {intent} at {index_path}")

    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": 8})
