import os

# System Environment Extraction
WEAVIATE_URL = os.environ.get("WEAVIATE_URL")
WEAVIATE_API_KEY = os.environ.get("WEAVIATE_API_KEY")
NGROK_OLLAMA_ENDPOINT = "***.ngrok-free.dev"

# Class Collection Token Configurations
COLLECTION_NAME = "CompetitorIntelligence"

def get_vector_schema_spec():
    """
    Returns an enterprise schema blueprint definition configured 
    with a text2vec engine routing matrix.
    """
    return {
        "name": COLLECTION_NAME,
        "description": "High-fidelity raw market indicators and raw competitor operational changes.",
        "properties": [
            {"name": "competitor", "dataType": "text", "description": "Target enterprise entity identifier."},
            {"name": "raw_insight", "dataType": "text", "description": "Unstructured parsed payload scraped from source data."},
            {"name": "category", "dataType": "text", "description": "Operational sector tag."},
            {"name": "timestamp", "dataType": "text", "description": "ISO execution log tracking time."}
        ]
    }
