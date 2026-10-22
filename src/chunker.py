
def chunk_pages(
    pages: list[dict],
    chunk_size: int = 700,
    overlap: int = 100,
) -> list[dict]:
    """Split PDF pages into overlapping chunks with source metadata."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    chunks = []
    step = chunk_size - overlap

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        for start in range(0, len(text), step):
            chunk_text = text[start:start + chunk_size].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "source": page["source"],
                    "page": page["page"],
                })

    return chunks
