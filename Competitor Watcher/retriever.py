import requests
import weaviate
from weaviate.classes.generate import GenerativeConfig
from config import COLLECTION_NAME, NGROK_OLLAMA_ENDPOINT

def run_hyde_retrieval(client: weaviate.WeaviateClient, operational_query: str) -> str:
    """
    Implements Hypothetical Document Embeddings (HyDE) to significantly enhance
    retrieval density profiles for non-deterministic production query pipelines.
    """
    print(f"🧠 Step 1: Generating hypothetical response model for query: '{operational_query}'...")
    
    hyde_generation_prompt = f"""
    Given the competitive intelligence query, write a fake paragraph detailing what a perfect, matching internal spy intelligence report or press leak snippet would look like. 
    Use industry buzzwords and realistic data structural layouts.
    
    [QUERY]: {operational_query}
    """
    
    payload = {
        "model": "llama3",
        "prompt": f"System: Write a realistic database entry.\nUser: {hyde_generation_prompt}\nResponse:",
        "stream": False
    }
    
    try:
        res = requests.post("http://localhost:11434/api/generate", json=payload, timeout=15)
        hypothetical_doc = res.json().get("response", "").strip()
        print(f"🔬 Generated Hypothetical Document Preview: {hypothetical_doc[:90]}...")
    except Exception as e:
        print(f"  ⚠️ HyDE step collapsed, falling back to raw text query: {e}")
        hypothetical_doc = operational_query

    print("🛰️ Step 2: Executing dense context cross-matching over Weaviate via ngrok...")
    collection = client.collections.use(COLLECTION_NAME)
    
    # Execute RAG synthesis using the rich hypothetical doc structure
    rag_prompt = f"Analyze the retrieved real intelligence reports. Formulate a strategic tactical response assessment recommendation matching this core query requirement: {operational_query}"
    
    response = collection.generate.near_text(
        query=hypothetical_doc,  # We feed the HYPOTHETICAL document to search for vector proximity matches!
        limit=2,
        grouped_task=rag_prompt,
        generative_provider=GenerativeConfig.ollama(
            api_endpoint=NGROK_OLLAMA_ENDPOINT,
            model="llama3"
        )
    )
    
    return response.generative.text
