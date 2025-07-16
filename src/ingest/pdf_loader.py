import os
import requests
from langchain_community.document_loaders import PyMuPDFLoader
from urllib.parse import urlparse
from tqdm import tqdm


def download_pdf(url, save_dir="pdfs"):
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.basename(urlparse(url).path)
    local_path = os.path.join(save_dir, filename)

    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            return local_path
        else:
            print(f"⚠️ Skipped (HTTP {response.status_code}): {url}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
    return None


def load_pdfs_from_file(file_path="src/ingest/links/useful_svnit_pdfs_without_newsletters.txt") -> list:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF links file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"📥 Downloading and loading {len(urls)} PDFs...")
    documents = []

    for url in tqdm(urls, desc="📄 Processing PDFs"):
        local_path = download_pdf(url)
        if local_path:
            try:
                loader = PyMuPDFLoader(local_path)
                documents.extend(loader.load())
            except Exception as e:
                print(f"❌ Failed to parse {local_path}: {e}")

    print(f"✅ Loaded {len(documents)} PDF documents")
    return documents
