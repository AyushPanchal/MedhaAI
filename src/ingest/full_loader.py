import os
import requests
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import RecursiveUrlLoader
from urllib.parse import urlparse
from pathlib import Path


def download_pdf(url: str, save_dir: str = "././pdfs/") -> str:
    os.makedirs(save_dir, exist_ok=True)
    filename = url.split("/")[-1]
    local_path = os.path.join(save_dir, filename)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Downloaded: {filename}")
            return local_path
        else:
            print(f"⚠️ Skipped (HTTP {response.status_code}): {url}")
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
    return None


def extract_pdf_links(docs):
    pdf_links = []
    for doc in docs:
        url = doc.metadata.get("source")
        if url and url.lower().endswith(".pdf"):
            pdf_links.append(url)
    return list(set(pdf_links))


def load_svnit_docs(start_url: str, max_depth: int = 2):
    # Step 1: Crawl HTML
    html_loader = RecursiveUrlLoader(
        url=start_url,
        max_depth=max_depth,
        use_async=False,
    )
    docs = html_loader.load()

    # Step 2: Extract PDF links
    pdf_urls = extract_pdf_links(docs)

    # Step 3: Download + load PDFs
    pdf_docs = []
    for url in pdf_urls:
        pdf_path = download_pdf(url)
        if pdf_path:
            try:
                loader = PyMuPDFLoader(pdf_path)
                pdf_docs.extend(loader.load())
            except Exception as e:
                print(f"❌ Failed to load PDF {pdf_path}: {e}")

    # Step 4: Merge all documents
    all_docs = docs + pdf_docs
    print(f"\n✅ Total loaded documents: {len(all_docs)} (HTML: {len(docs)}, PDF: {len(pdf_docs)})")
    return all_docs
