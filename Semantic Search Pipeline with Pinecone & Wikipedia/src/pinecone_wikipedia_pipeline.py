import os
import sys
import time
from datasets import load_dataset
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# 1. Secure Credential Loading
# Fetch the API key natively from the OS environment to safeguard credentials
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    print("❌ ERROR: PINECONE_API_KEY environment variable not found.")
    print("Please set it in your terminal before running: export PINECONE_API_KEY='your_key'")
    sys.exit(1)

# Indexing Configurations
INDEX_NAME = "wikipedia-recursive-stream"
NAMESPACE = "wikipedia-articles"

# Initialize the Pinecone Client
pc = Pinecone(api_key=PINECONE_API_KEY)

# 2. Initialize the Cognitive Components
print("⏳ Initializing local Hugging Face embedding model (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
VECTOR_DIMENSION = 384  # Matches all-MiniLM-L6-v2's output footprint exactly

# Define LangChain's hierarchical recursive text splitter
print("⏳ Configuring LangChain RecursiveCharacterTextSplitter...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,        # Optimized character length per chunk for complex rule context
    chunk_overlap=100,      # Sliding window buffer to maintain semantic context boundaries
    length_function=len,
    separators=["\n\n", "\n", " ", ""]  # Hierarchical breakdown rules
)

# 3. Handle Pinecone Index Lifecycle
print(f"⏳ Verification: Validating index status for '{INDEX_NAME}'...")
if INDEX_NAME not in [index.name for index in pc.list_indexes()]:
    print(f"✨ Index '{INDEX_NAME}' not found. Spawning cloud serverless index...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=VECTOR_DIMENSION,
        metric="cosine",  # Optimal metric for measuring structural concept angles
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    while not pc.describe_index(INDEX_NAME).status['ready']:
        time.sleep(1)
    print("✅ Serverless index initialized and online!")

index = pc.Index(INDEX_NAME)

# 4. Stream, Filter, and Split Data
print("⏳ Streaming dataset records from Hugging Face (wikimedia/wikipedia)...")
raw_dataset = load_dataset("wikimedia/wikipedia", "20231101.en", split="train", streaming=True)

# Define target domain keywords to avoid semantic drift
BOARD_GAME_KEYWORDS = {"chess", "board game", "checkmate", "tabletop game"}

print("Searching for board game articles...")
matched_articles_count = 0
MAX_ARTICLES_TO_INDEX = 20  # Stream past 'A' to capture deep domain targets like 'Chess'
processed_count = 0

print("🚀 Splitting raw data via LangChain chunking infrastructure...")

try:
    for article in raw_dataset:
        # Safely extract text strings
        article_title = article.get("title", "Unknown")
        article_text = article.get("text", "")
        article_id = article.get("id", str(processed_count))
        
        # Standardize strings to lowercase for robust matching criteria
        title_lower = article_title.lower()
        text_preview_lower = article_text[:500].lower()
        
        # Check if this article belongs to our target board game ecosystem
        if any(k in title_lower for k in BOARD_GAME_KEYWORDS) or any(k in text_preview_lower for k in BOARD_GAME_KEYWORDS):

            # Use LangChain to break down massive documents cleanly into contextual sub-strings
            chunks = text_splitter.split_text(article_text)
            print(f"🚀 Found Match! Splitting '{article_title}': Generated {len(chunks)} fragments.")
            
            vectors_to_upsert = []
            
            # Compile processing arrays exclusively for matching documents
            for idx, chunk_text in enumerate(chunks):
                # Convert structural text fragment into dense float vector matrices
                vector_embedding = embedding_model.encode(chunk_text).tolist()
                
                # Package standard payload format for Pinecone
                vectors_to_upsert.append({
                    "id": f"wiki_{article_id}_chunk_{idx}",
                    "values": vector_embedding,
                    "metadata": {
                        "title": article_title,
                        "text": chunk_text
                    }
                })
                
            # 5. Pipeline Dispatch (Upsert in loop per-article to insulate against cafe latency failures)
            if vectors_to_upsert:
                print(f" └─ Uploading {len(vectors_to_upsert)} fragments to Pinecone...")
                index.upsert(vectors=vectors_to_upsert, namespace=NAMESPACE, timeout=60)
            
            matched_articles_count += 1
            
        processed_count += 1

        # Break the pipeline loop when you have fully processed enough MATCHING articles
        if matched_articles_count >= MAX_ARTICLES_TO_INDEX:
            print(f"\n✅ Successfully found, processed, and uploaded {MAX_ARTICLES_TO_INDEX} target articles.")
            break

except Exception as e:
    # Captures stream socket terminations from cafe network dropouts or early loop breaks smoothly
    print(f"\n⚠️ Note: Streaming network socket closed or interrupted ({e}).")
    print("Advancing pipeline with the data successfully indexed up to this point...")

print("✅ Pipeline sync complete!")

# Give background indices a quick moment to finalize placement coordinates
time.sleep(3)

# 6. Execute Multi-Word Semantic Probe
user_query = "What rules apply to competitive board games involving checkmate?"
print(f"\n🔍 Testing Vector Search Query: '{user_query}'")

query_vector = embedding_model.encode(user_query).tolist()
search_results = index.query(
    namespace=NAMESPACE,
    vector=query_vector,
    top_k=2,
    include_metadata=True
)

print("\n🎯 --- SEMANTIC SEARCH HITS RETRIEVED ---")
for idx, match in enumerate(search_results["matches"]):
    print(f"\n[{idx + 1}] Source Doc: '{match['metadata']['title']}' (Vector Match: {round(match['score'] * 100, 2)}%)")
    print(f"    Text Payload: {match['metadata']['text']}")
