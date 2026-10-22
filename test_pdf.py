
from src.pdf_loader import extract_text

pdf_path = "sample_docs/handbook.pdf"

pages = extract_text(pdf_path)

print(f"Pages with extractable text: {len(pages)}")
print(f"First page number: {pages[0]['page']}")
print(f"Source: {pages[0]['source']}")
print("\nExtracted text preview:\n")
print(pages[0]["text"][:1000])
