import os
from langchain_community.document_loaders import WebBaseLoader


def load_html_from_file(file_path: str = r"links\html_links.txt") -> list:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"HTML links file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"📥 Loading {len(urls)} HTML pages using WebBaseLoader...")

    loader = WebBaseLoader(urls)
    documents = loader.load()

    print(f"✅ Loaded {len(documents)} HTML documents")
    return documents
