from src.ingest.html_loader import load_html_from_file
from src.ingest.pdf_loader import load_pdfs_from_file


# Had to include absolute paths because referential paths were not working.
html_docs = load_html_from_file(r"C:\Users\Ayush\OneDrive\Desktop\MedhaAI\src\ingest\links\html_links.txt")
pdf_docs = load_pdfs_from_file(r"C:\Users\Ayush\OneDrive\Desktop\MedhaAI\src\ingest\links\pdf_links.txt")

print(f"✅ HTML Loaded: {len(html_docs)}")
print(f"✅ PDFs Loaded: {len(pdf_docs)}")
print(f"📦 Total Documents: {len(html_docs) + len(pdf_docs)}")
