
from src.rag_pipeline import answer_question


question = "How do I open a file in Python?"

try:
    result = answer_question(question)

    print("\nQUESTION")
    print(question)

    print("\nANSWER")
    print(result["answer"])

    print("\nSOURCES")

    for source in result["sources"]:
        print(
            f"- {source['source']}, "
            f"page {source['page']}, "
            f"distance {source['distance']:.4f}"
        )

except Exception as exc:
    print(f"RAG test failed: {type(exc).__name__}: {exc}")
