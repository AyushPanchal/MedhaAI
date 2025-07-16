from typing import List
from langchain_community.document_loaders import WebBaseLoader, PyMuPDFLoader
from urllib.parse import urlparse
import os
import requests

from src.config.intent_links import INTENT_LINK_MAP

PDF_DIR = "pdfs"


def is_pdf(url: str) -> bool:
    return url.lower().endswith(".pdf")


def download_pdf(url: str, save_dir: str = PDF_DIR) -> str:
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


def load_intent_documents(intent_name: str) -> List:
    from tqdm import tqdm

    if intent_name not in INTENT_LINK_MAP:
        raise ValueError(f"Intent '{intent_name}' not found in INTENT_LINK_MAP")

    urls = INTENT_LINK_MAP[intent_name]
    html_urls = [u for u in urls if not is_pdf(u)]
    pdf_urls = [u for u in urls if is_pdf(u)]

    all_documents = []

    # Load HTML pages
    if html_urls:
        print(f"🌐 Loading {len(html_urls)} HTML URLs for intent '{intent_name}'...")
        html_loader = WebBaseLoader(html_urls)
        all_documents.extend(html_loader.load())

    # Load and parse PDFs
    if pdf_urls:
        print(f"📄 Downloading + parsing {len(pdf_urls)} PDFs for intent '{intent_name}'...")
        for url in tqdm(pdf_urls, desc="PDFs"):
            local_path = download_pdf(url)
            if local_path:
                try:
                    loader = PyMuPDFLoader(local_path)
                    all_documents.extend(loader.load())
                except Exception as e:
                    print(f"❌ Could not parse {local_path}: {e}")

    print(f"✅ Total documents loaded for '{intent_name}': {len(all_documents)}")
    return all_documents
