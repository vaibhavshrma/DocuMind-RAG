# DocuMind-RAG 📚

### Chat with your PDF documents using Retrieval-Augmented Generation (RAG)

DocuMind is a Python-based document question-answering application that allows users to upload PDF documents and ask questions about their content. It retrieves relevant passages using semantic search and generates answers with a locally running Large Language Model (LLM).

The project uses a local AI model through Ollama, so it does not require paid OpenAI API credits.

## ✨ Features

- **PDF Text Extraction:** Extracts readable text from uploaded PDF documents.
- **Text Chunking:** Splits extracted content into smaller, overlapping chunks for retrieval.
- **Semantic Search:** Uses Sentence Transformers to create embeddings and ChromaDB to find relevant passages.
- **Local LLM Inference:** Generates answers using Llama 3.2 3B through Ollama.
- **Source References:** Preserves document names and page numbers so retrieved passages can be inspected.
- **Interactive Web Interface:** Provides a Streamlit interface for uploading PDFs and asking questions.
- **Local Processing:** Runs embeddings, vector search, and language-model inference locally.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web interface |
| PyPDF | PDF text extraction |
| Sentence Transformers | Text embeddings |
| ChromaDB | Vector storage and similarity search |
| Ollama | Local LLM runtime |
| Llama 3.2 3B | Answer generation |

## 🧠 How It Works

1. **Upload:** The user uploads a PDF document.
2. **Extract:** DocuMind extracts readable text and page metadata.
3. **Chunk:** The extracted text is divided into smaller overlapping passages.
4. **Embed:** Sentence Transformers converts the passages into vector embeddings.
5. **Index:** ChromaDB stores the passages and their metadata for similarity search.
6. **Retrieve:** The user's question is embedded and matched against relevant passages.
7. **Generate:** Ollama runs Llama 3.2 3B to generate an answer based on the retrieved context.
8. **Inspect Sources:** The interface displays the answer and retrieved source passages.

## 🏗️ Project Structure

```text
DocuMind-RAG/
├── app.py
├── test_rag.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── vector_store.py
│   └── rag_pipeline.py
└── sample_docs/
```

The `chroma_db/` directory is generated locally when the vector index is created and is excluded from version control.

## ⚙️ Prerequisites

- Python 3.10 or a compatible version for the installed dependencies
- Git
- Ollama installed on your computer
- Sufficient RAM and CPU resources to run the selected language model

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DocuMind-RAG.git
cd DocuMind-RAG
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Download the language model

Make sure Ollama is installed and available in your terminal. Then run:

```powershell
ollama pull llama3.2:3b
```

The model download requires an internet connection. Once downloaded, inference runs locally.

### 5. Start the application

From the project root, run:

```powershell
python -m streamlit run app.py
```

Open the local URL printed in your terminal by Streamlit.

### 6. Use DocuMind

1. Upload a text-based PDF document.
2. Click **Process PDF** to extract, chunk, embed, and index its content.
3. Enter a question about the document.
4. Click **Ask DocuMind** to generate an answer.
5. Inspect the retrieved source passages and page numbers.

## 🧪 Testing

Run the RAG pipeline test, if included in the repository:

```powershell
python test_rag.py
```

You can also check Python syntax with:

```powershell
python -m py_compile app.py src\pdf_loader.py src\chunker.py src\vector_store.py src\rag_pipeline.py
```

## ⚠️ Limitations

- Response speed depends on the available hardware and the selected language model. CPU-only inference may be slow.
- Scanned PDFs without an embedded text layer may require OCR, which is not currently included.
- Answer quality depends on the source document, retrieval results, and language model. Generated answers should be checked against the source passages.
- The current implementation indexes the active uploaded document in a local vector database. Persistent multi-user document management is not implemented.

## 🔮 Potential Future Improvements

- Add OCR support for scanned PDFs.
- Improve retrieval using reranking and configurable chunking.
- Add streaming responses and response-time measurements.
- Support multiple documents and persistent document collections.
- Add automated tests for extraction, retrieval, and answer generation.
- Deploy the application with appropriate resource and privacy considerations.

## 👨‍💻 Project Purpose

DocuMind was developed as a hands-on project to explore Retrieval-Augmented Generation, semantic search, vector databases, local LLM inference, and document-processing workflows using Python.

## 📄 License

A license has not yet been selected. Add a license file before presenting the repository as open source.
