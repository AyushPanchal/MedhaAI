import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.config.intent_links import INTENT_LINK_MAP
from src.ingest.intent_loader import load_intent_documents
from dotenv import load_dotenv

load_dotenv()

INDEX_BASE_DIR = "../../faiss_indexes"


def build_all_indexes():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    for intent, links in INTENT_LINK_MAP.items():
        print(f"\n🔍 Building FAISS index for: {intent} ({len(links)} links)")
        try:
            documents = load_intent_documents(intent)
            if not documents:
                print(f"⚠️ Skipping '{intent}' — no documents loaded.")
                continue

            vectorstore = FAISS.from_documents(documents, embeddings)

            save_path = os.path.join(INDEX_BASE_DIR, f"{intent}_index")
            vectorstore.save_local(save_path)
            print(f"✅ Saved FAISS index to: {save_path}")
        except Exception as e:
            print(f"❌ Error processing '{intent}': {e}")


if __name__ == "__main__":
    build_all_indexes()
