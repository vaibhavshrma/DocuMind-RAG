
from src.pdf_loader import extract_text
from src.chunker import chunk_pages

pages = extract_text("sample_docs/handbook.pdf")
chunks = chunk_pages(pages, chunk_size=700, overlap=100)

print(f"Extracted pages: {len(pages)}")
print(f"Created chunks: {len(chunks)}")

for index, chunk in enumerate(chunks[:3], start=1):
    print(f"\n--- Chunk {index} ---")
    print(f"Source: {chunk['source']}")
    print(f"Page: {chunk['page']}")
    print(chunk["text"][:200])
