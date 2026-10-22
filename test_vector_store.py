
from src.pdf_loader import extract_text
from src.chunker import chunk_pages
from src.vector_store import create_index, search_chunks


pdf_path = "Sample_docs/handbook.pdf"

pages = extract_text(pdf_path)
chunks = chunk_pages(pages, chunk_size=700, overlap=100)

print(f"Chunks prepared: {len(chunks)}")

count = create_index(chunks)
print(f"Chunks stored in ChromaDB: {count}")

question = "How do I work with files in Python?"

results = search_chunks(question, top_k=3)

print(f"\nQuestion: {question}")

for index, result in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print(f"Source: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Cosine distance: {result['distance']:.4f}")
    print(result["text"][:500])
