
from pathlib import Path
from pypdf import PdfReader


def extract_text(pdf_path: str) -> list[dict]:
    """Extract text and page metadata from a PDF."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Please provide a PDF file.")

    reader = PdfReader(str(path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "text": text,
                "page": page_number,
                "source": path.name,
            })

    if not pages:
        raise ValueError(
            "No extractable text found. The PDF may be scanned "
            "and require OCR."
        )

    return pages