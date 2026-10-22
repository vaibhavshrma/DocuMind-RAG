
from src.pdf_loader import extract_text

pages = extract_text("Sample_docs/handbook.pdf")

for page in pages:
    text = page["text"]

    print(f"\nPage {page['page']}")
    print(f"Characters: {len(text)}")
    print(f"Readable English/Hindi sample: {text[:250]}")
    print(f"Replacement characters: {text.count(chr(0xFFFD))}")
