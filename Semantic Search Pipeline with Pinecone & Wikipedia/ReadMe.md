# Semantic Search Pipeline with Pinecone & Wikipedia

A robust data engineering and retrieval pipeline that streams Wikipedia data, filters for specific domain knowledge (Chess & Board Games), chunks the text structurally, and indexes dense vector embeddings into Pinecone for high-accuracy semantic search.

## Purpose

The primary objective of this project is to implement and optimize an end-to-end Retrieval-Augmented Generation (RAG) style ingestion pipeline. 

The script streams live records from Hugging Face's global Wikipedia dataset, isolating articles mapped to specific target domains (such as competitive chess and tabletop gaming) to eliminate semantic drift. The text is recursively fragmented into context-retaining chunks, embedded locally using a deep learning transformer model, and upserted into a cloud-native serverless Pinecone index. 

Finally, the system runs semantic probes to return contextually accurate answers to complex domain queries, such as: 
> *"What rules apply to competitive board games involving checkmate?"*

---

## Built With

* **Python 3.12+** - Core language infrastructure
* **Pinecone DB** - Cloud serverless vector database for floating-point matrix indexing
* **LangChain** - `RecursiveCharacterTextSplitter` architecture for structural chunking
* **Hugging Face `datasets`** - Real-time streaming interface for the Wikipedia dataset
* **Sentence-Transformers** - `all-MiniLM-L6-v2` local embedding engine

---

## Setup

Ensure you have your Pinecone API key set in your local environment variables before running the pipeline:

export PINECONE_API_KEY="your-pinecone-api-key-here"

Set up Python environment: 

python3 -m venv .venv

source .venv/bin/activate

Install the required dependencies using your active environment's package manager:

pip install datasets langchain-text-splitters pinecone-client sentence-transformers torch

Run the core pipeline to stream data, build the index, and execute the test semantic query:

python pinecone_wikipedia_pipeline.py

## Sample Output 

🔍 Testing Vector Search Query: 'What rules apply to competitive board games involving checkmate?'

🎯 --- SEMANTIC SEARCH HITS RETRIEVED ---

[1] Source Doc: 'Chess' (Vector Match: 60.55%)
    Text Payload: Endgames can be classified according to the type of pieces remaining on the board. Basic checkmates are positions in which one side has only a king and the other side has one or two pieces and can checkmate the opposing king, with the pieces working together with their king. For example, king and pawn endgames involve only kings and pawns on one or both sides, and the task of the stronger side is to promote one of the pawns. Other more complicated endings are classified according to pieces on the board other than kings, such as "rook and pawn versus rook" endgames.

[2] Source Doc: 'Chess' (Vector Match: 60.36%)
    Text Payload: Dead position: If neither player is able to checkmate the other by any legal sequence of moves, the game is drawn. For example, if only the kings are on the board, all other pieces having been captured, checkmate is impossible, and the game is drawn by this rule. On the other hand, if both players still have a knight, there is a highly unlikely yet theoretical possibility of checkmate, so this rule does not apply. The dead position rule supersedes the previous rule which referred to "insufficient material", extending it to include other positions where checkmate is impossible, such as
