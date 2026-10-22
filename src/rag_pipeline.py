
import ollama

from src.vector_store import search_chunks


MODEL_NAME = "llama3.2:3b"


def answer_question(
    question: str,
    top_k: int = 3,
) -> dict:
    """
    Retrieve relevant document passages and generate
    an answer using a local Ollama language model.
    """

    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    # Step 1: Retrieve evidence from ChromaDB.
    sources = search_chunks(question, top_k=top_k)

    if not sources:
        return {
            "answer": (
                "I couldn't find relevant information "
                "in the documents."
            ),
            "sources": [],
        }

    # Step 2: Prepare context with source citations.
    context_parts = []

    for index, source in enumerate(sources, start=1):
        context_parts.append(
            f"[Source {index}: {source['source']}, "
            f"page {source['page']}]\n"
            f"{source['text']}"
        )

    context = "\n\n".join(context_parts)

    # Step 3: Generate the answer locally using Ollama.

    
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are DocuMind, a document question-answering "
                    "assistant. Answer using only the supplied "
                    "document excerpts. If the answer is not present, "
                    "say so. Be concise and cite sources as [Source 1]."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Document excerpts:\n{context}"
                ),
            },
        ],
        options={
            "temperature": 0,
            "num_predict": 180,
            "num_ctx": 2048,
        },
        keep_alive="30m",
    )


    answer = response.message.content or ""

    # Step 4: Return the answer and original source metadata.
    return {
        "answer": answer,
        "sources": sources,
    }
