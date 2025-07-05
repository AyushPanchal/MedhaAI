import os
import re
import urllib.parse
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader


def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()


def get_child_urls(parent_url: str, max_depth: int = 1000):
    loader = RecursiveUrlLoader(
        url=parent_url,
        max_depth=max_depth,
        extractor=bs4_extractor,
        continue_on_failure=True,
        check_response_status=True,
        autoset_encoding=True
    )

    documents = loader.lazy_load()

    pdf_urls = []
    html_urls = []

    print("🔍 Crawling using RecursiveUrlLoader...\n")
    for doc in tqdm(documents, desc="🔗 Analyzing URLs"):
        raw_url = doc.metadata.get("source", "")
        url = urllib.parse.quote(raw_url, safe=':/')

        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            content_type = response.headers.get("Content-Type", "").lower()

            if response.status_code == 200:
                if "application/pdf" in content_type or url.lower().endswith(".pdf"):
                    print(f"📄 PDF Found:  {url}")
                    pdf_urls.append(url)
                elif "text/html" in content_type or url.lower().endswith((".html", ".php", ".net")):
                    print(f"📝 HTML Found: {url}")
                    html_urls.append(url)

        except requests.RequestException as e:
            print(f"⚠️ Skipped: {url} — {e}")
            continue

    return sorted(set(html_urls)), sorted(set(pdf_urls))


def save_links(html_links, pdf_links, folder="links"):
    os.makedirs(folder, exist_ok=True)
    html_path = os.path.join(folder, "html_links.txt")
    pdf_path = os.path.join(folder, "pdf_links.txt")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_links))

    with open(pdf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(pdf_links))

    print(f"\n✅ Saved {len(html_links)} HTML links to {html_path}")
    print(f"✅ Saved {len(pdf_links)} PDF links to {pdf_path}")


if __name__ == "__main__":
    START_URL = "https://www.svnit.ac.in/web/department/computer/"
    html_links, pdf_links = get_child_urls(START_URL, max_depth=1000)
    save_links(html_links, pdf_links)
