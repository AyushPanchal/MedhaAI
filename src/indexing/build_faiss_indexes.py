import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.config.intent_links import INTENT_LINK_MAP
from src.ingest.intent_loader import load_html_from_links, load_pdfs_from_links  # Your new utility functions

def build_faiss_index_for_intent(intent_name: str, save_dir: str = "faiss_indexes"):
    # Get URLs for this intent
    urls = INTENT_LINK_MAP.get(intent_name, [])
    if not urls:
        print(f"❌ No links found for intent: {intent_name}")
        return

    # Separate PDF and HTML links
    pdf_links = [url for url in urls if url.lower().endswith(".pdf")]
    html_links = [url for url in urls if not url.lower().endswith(".pdf")]

    # Load documents
    documents = []
    if pdf_links:
        print(f"🔍 Loading {len(pdf_links)} PDF links...")
        documents.extend(load_pdfs_from_links(pdf_links))
    if html_links:
        print(f"🌐 Loading {len(html_links)} HTML links...")
        documents.extend(load_html_from_links(html_links))

    if not documents:
        print("⚠️ No documents loaded. Exiting.")
        return

    print(f"🧠 Embedding {len(documents)} documents...")

    # Create FAISS index
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = FAISS.from_documents(documents, embedding=embeddings)

    # Save index
    os.makedirs(save_dir, exist_ok=True)
    index_path = os.path.join(save_dir, f"{intent_name}_index")
    vectorstore.save_local(index_path)

    print(f"✅ Saved FAISS index to: {index_path}")


# Run for a single intent
if __name__ == "__main__":
    build_faiss_index_for_intent("faculty_details")
