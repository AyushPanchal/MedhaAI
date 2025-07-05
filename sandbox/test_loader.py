from src.ingest.full_loader import load_svnit_docs

docs = load_svnit_docs("https://www.svnit.ac.in/web/department/computer/", max_depth=2)

print("\n🔎 Sample:")
print(docs[0].metadata)
print(docs[0].page_content[:300])
