
import streamlit as st
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.pdf_loader import extract_text
from src.chunker import chunk_pages
from src.vector_store import create_index
from src.rag_pipeline import answer_question


st.set_page_config(
    page_title="DocuMind | PDF Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 DocuMind")
st.subheader("Chat with your PDF documents")
st.write(
    "Upload a PDF, build its search index, "
    "and ask questions using a local AI model."
)

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
)

if uploaded_file is not None:
    if st.button("Process PDF", type="primary"):
        temp_path = None

        try:
            with NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = Path(temp_file.name)

            with st.spinner("Reading and indexing your PDF..."):
                pages =  extract_text(str(temp_path))
                chunks = chunk_pages(pages)
                count = create_index(chunks)

            st.session_state.indexed = True
            st.session_state.chat_history = []
            st.session_state.document_name = uploaded_file.name

            st.success(
                f"Successfully indexed {uploaded_file.name}. "
                f"Created {count} searchable chunks."
            )

        except Exception as exc:
            st.error(f"Could not process the PDF: {exc}")

        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

if st.session_state.indexed:
    st.divider()
    st.success(
        f"Active document: {st.session_state.document_name}"
    )

    question = st.text_input(
        "Ask a question about your document",
        placeholder="e.g. How do I open a file in Python?",
    )

    if st.button("Ask DocuMind"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Searching your document and generating an answer..."):
                    result = answer_question(question)

                st.session_state.chat_history.append({
                    "question": question,
                    "answer": result["answer"],
                    "sources": result["sources"],
                })

            except Exception as exc:
                st.error(f"Could not generate an answer: {exc}")

    for item in reversed(st.session_state.chat_history):
        st.markdown("### You asked")
        st.write(item["question"])

        st.markdown("### DocuMind's answer")
        st.markdown(item["answer"])

        with st.expander("View source passages"):
            if item["sources"]:
                for source in item["sources"]:
                    st.markdown(
                        f"**{source['source']} — Page {source['page']}**"
                    )
                    st.write(source["text"])
                    st.caption(
                        f"Retrieval distance: {source['distance']:.4f}"
                    )
                    st.divider()
            else:
                st.write("No source passages were returned.")
