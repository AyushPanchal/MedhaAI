from src.ingest.html_loader import load_html_from_file
from src.ingest.pdf_loader import load_pdfs_from_file
from src.vectorestore.embedding_pipeline import chunk_documents, embed_and_store

# 1. Load
docs = load_html_from_file(r"C:\Users\Ayush\OneDrive\Desktop\MedhaAI\src\ingest\links\useful_svnit_urls.txt") + load_pdfs_from_file(r"C:\Users\Ayush\OneDrive\Desktop\MedhaAI\src\ingest\links\useful_svnit_pdfs_without_newsletters.txt")

# 2. Chunk
chunks = chunk_documents(docs, chunk_size=1000, chunk_overlap=200)

# 3. Embed + Store
vs = embed_and_store(chunks)
