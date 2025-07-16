import os
from typing import List
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import pickle
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-large"
INDEX_DIR = "faiss_index"


# 1. Split documents
def chunk_documents(documents: List[Document], chunk_size=1000, chunk_overlap=200):
    print(f"🔪 Chunking {len(documents)} documents...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Chunked into {len(chunks)} total chunks.")
    return chunks


# 2. Embed and store in FAISS
def embed_and_store(chunks: List[Document], persist_dir: str = INDEX_DIR):
    print(f"🧠 Generating embeddings with OpenAI ({EMBEDDING_MODEL})...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(persist_dir, exist_ok=True)
    faiss_file = os.path.join(persist_dir, "index.faiss")
    store_file = os.path.join(persist_dir, "store.pkl")

    print(f"💾 Saving FAISS index to: {faiss_file}")
    vectorstore.save_local(persist_dir)

    # Optional: also save chunks metadata
    with open(store_file, "wb") as f:
        pickle.dump(chunks, f)

    print("✅ Vectorstore saved and ready.")

    return vectorstore
