from src.ingest.intent_loader import load_intent_documents
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

from dotenv import load_dotenv

load_dotenv()

intent = "faculty_details"
save_dir = os.path.join("sandbox_indexes", f"{intent}_index")

docs = load_intent_documents(intent)
if docs:
    print(f"✅ Loaded {len(docs)} documents. Embedding...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(save_dir)
    print(f"📁 Index saved at {save_dir}")
else:
    print("❌ No documents found.")
