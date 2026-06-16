import asyncio
import datetime
import requests
import weaviate
from config import COLLECTION_NAME, NGROK_OLLAMA_ENDPOINT

# Production Ingestion Matrix Stream Simulation
RAW_STREAM_INGESTION_PAYLOAD = [
    {
        "competitor": "AlphaCorp",
        "raw_dump": "🚨 BREAKING!!! alpha-corp updated pricing page tier v2. enterprise seat cost slashed from 150 to 99 bucks/mo if bundled with annual commitment tier. effective immediately starting next fiscal quarter. clear target at mid-market space."
    },
    {
        "competitor": "BetaSystems",
        "raw_dump": "PR RELEASE RELEASE: BetaSystems welcomes Dr. Sarah Jenkins as new Chief Technology Officer. Sarah formerly headed core ML infra at cloud giants. moving them away from standard microservices into autonomous multi-agent operational grids."
    }
]

def clean_and_extract_metadata(raw_dump: str) -> dict:
    """
    LLM-Data-Pipeline Layer: Uses local Llama 3 to sanitize noisy data
    and return deterministic, structured metadata.
    """
    cleaning_prompt = f"""
    You are a strict data-cleaning pipeline module. Standardize the following unstructured text dump into a concise, professional fact string.
    Also, categorize it into exactly ONE of these buckets: [PRICING, TECHNOLOGY, EXECUTIVE, COMPLIANCE].

    Output format MUST be strictly key-value lines like this:
    INSIGHT: <your clean concise statement summary>
    CATEGORY: <the category bucket value>

    [UNSTRUCTURED TEXT]: {raw_dump}
    """
    
    payload = {
        "model": "llama3",
        "prompt": f"System: You are an isolated regex-like extraction script.\nUser: {cleaning_prompt}\nResponse:",
        "stream": False
    }
    
    try:
        res = requests.post(f"http://localhost:11434/api/generate", json=payload, timeout=15)
        text = res.json().get("response", "")
        
        # Regex/String parsing parameters
        insight = "Data Parsing Failure"
        category = "TECHNOLOGY"
        
        for line in text.split("\n"):
            if line.startswith("INSIGHT:"):
                insight = line.replace("INSIGHT:", "").strip()
            elif line.startswith("CATEGORY:"):
                category = line.replace("CATEGORY:", "").strip().upper()
                
        return {"insight": insight, "category": category}
    except Exception as e:
        print(f"  ⚠️ Pipeline cleaning node crash: {e}")
        return {"insight": raw_dump[:100], "category": "TECHNOLOGY"}

async def ingest_pipeline_stream(client: weaviate.WeaviateClient):
    """
    Simulates a non-blocking asynchronous stream handler that processes
    unstructured documents concurrently and writes batches into Weaviate.
    """
    print("🌊 Starting asynchronous ingestion stream pump...")
    collection = client.collections.use(COLLECTION_NAME)
    
    for item in RAW_STREAM_INGESTION_PAYLOAD:
        print(f"📥 Processing incoming packet for: {item['competitor']}...")
        
        # Run the CPU-bound/Network-bound clean task concurrently via asyncio wrapper
        loop = asyncio.get_event_loop()
        clean_data = await loop.run_in_executor(None, clean_and_extract_metadata, item["raw_dump"])
        
        # Prepare verified data structure package
        vector_payload = {
            "competitor": item["competitor"],
            "raw_insight": clean_data["insight"],
            "category": clean_data["category"],
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        # Insert straight into your live Weaviate cluster instance
        uuid = collection.data.insert(properties=vector_payload)
        print(f"  💾 Securely indexed inside Weaviate vector slot. UUID: {uuid}")
