
import hashlib
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
DB_PATH = "chroma_db"
COLLECTION_NAME = "documind"

# Load the embedding model once per Python process.
_model = None


def get_embedding_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def create_index(
    chunks: list[dict],
    db_path: str = DB_PATH,
) -> int:
    """Embed chunks and save them in a persistent ChromaDB collection."""

    if not chunks:
        raise ValueError("No chunks were provided.")

    model = get_embedding_model()
    client = chromadb.PersistentClient(path=db_path)

    # Rebuild the prototype index to prevent stale chunks.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception as exc:
        # Ignore only the case where the collection doesn't exist.
        if "does not exist" not in str(exc).lower():
            raise

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).tolist()

    ids = []
    metadatas = []

    for chunk in chunks:
        identity = (
            f"{chunk['source']}|{chunk['page']}|{chunk['text']}"
        )
        chunk_id = hashlib.sha256(
            identity.encode("utf-8")
        ).hexdigest()

        ids.append(chunk_id)
        metadatas.append({
            "source": chunk["source"],
            "page": int(chunk["page"]),
        })

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return collection.count()


def search_chunks(
    question: str,
    db_path: str = DB_PATH,
    top_k: int = 3,
) -> list[dict]:
    """Return the most relevant chunks for a question."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    client = chromadb.PersistentClient(path=db_path)

    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = get_embedding_model().encode(
        question,
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]

        matches.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": results["distances"][0][i],
        })

    return matches
