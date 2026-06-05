# Personal Knowledge Assistant (RAG)

A Retrieval-Augmented Generation (RAG) project built with LangChain, ChromaDB, and local HuggingFace embeddings.
The application ingests personal documents (CVs, project notes, PDFs), chunks them into semantic units, generates vector embeddings, stores them in ChromaDB, and retrieves the most relevant information in response to user questions.

# Features
- PDF document ingestion
- Recursive text chunking
- Local embedding generation using HuggingFace
- Vector storage with ChromaDB
- Semantic similarity search
- Modular architecture for future LLM integration

# Architecture

<img width="849" height="122" alt="Screenshot 2026-06-05 at 16 37 00" src="https://github.com/user-attachments/assets/b041fb64-e2fc-443d-8c9d-84dc2a168e86" />

# Tech Stack
- Python
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers

# Installation

Clone the repository:

git clone

cd personal-knowledge-assistant

Create a virtual environment:

python -m venv venv

source venv/bin/activate

# Running the Project
Place PDF files inside:
knowledge base/

Run:

python src/main.py

The application will:

1. Load all PDF documents
2. Chunk the documents
3. Generate embeddings
4. Store vectors in ChromaDB
5. Execute similarity search
6. Return relevant document chunks

Example Query

Question:

"What companies have I worked for?"

# Future Improvements

LLM answer generation using Ollama or OpenAI

# Key Learnings

This project demonstrates understanding of:

- Retrieval-Augmented Generation (RAG)
- Vector databases
- Semantic search
- Embedding models
- Document preprocessing
- AI workflow architecture
