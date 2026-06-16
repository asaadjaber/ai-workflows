import asyncio
import os
import weaviate
from config import WEAVIATE_URL, WEAVIATE_API_KEY, COLLECTION_NAME, get_vector_schema_spec, NGROK_OLLAMA_ENDPOINT
from ingestion_pump import ingest_pipeline_stream
from retriever import run_hyde_retrieval

async def main():
    print("🚀 Initializing 'Shadow AI' Corporate Watcher Engine v1.0...")
    
    if not WEAVIATE_URL or not WEAVIATE_API_KEY:
        print("❌ Error: Missing environment variables for Weaviate credentials.")
        return

    # Connect to the cloud cluster engine interface
    with weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=WEAVIATE_API_KEY
    ) as client:
        
        print(f"📝 Mapping out vector schema structural definition for {COLLECTION_NAME}...")
        
        # Define properties using explicit stable v4 types
        properties_config = [
            weaviate.classes.config.Property(name="competitor", data_type=weaviate.classes.config.DataType.TEXT),
            weaviate.classes.config.Property(name="raw_insight", data_type=weaviate.classes.config.DataType.TEXT),
            weaviate.classes.config.Property(name="category", data_type=weaviate.classes.config.DataType.TEXT),
            weaviate.classes.config.Property(name="timestamp", data_type=weaviate.classes.config.DataType.TEXT)
        ]
        
        # Configure the collection to handle auto-vectorization locally
        client.collections.create(
            name=COLLECTION_NAME,
            description="High-fidelity raw market indicators.",
            properties=properties_config,
            
            #  FIX: Route embedding requests to the dedicated local embedding model
            vectorizer_config=weaviate.classes.config.Configure.Vectorizer.text2vec_ollama(
                api_endpoint=NGROK_OLLAMA_ENDPOINT,
                model="nomic-embed-text" # Dedicated embedding translation layer
            )
        )
        print("✅ Production collection vector space online with active vectorizer matrix.")
        print("-" * 60)
        
        # 1. Trigger non-blocking data injection pipeline
        await ingest_pipeline_stream(client)
        print("-" * 60)
        
        # Allow the data layer time to settle and commit logs
        await asyncio.sleep(2)
        
        # 2. Execute deep vector cross-lookup via advanced HyDE pipelines
        user_analytical_query = "Summarize any cost structural updates or price cuts that impact our mid-market pricing strategies."
        
        print(f"🔎 Injecting tactical operations deep-query request: '{user_analytical_query}'")
        strategic_report = run_hyde_retrieval(client, user_analytical_query)
        
        print("\n" + "="*60)
        print("📊 [FINAL COMPETITIVE INTELLIGENCE EXECUTIVE UPDATE]")
        print("="*60)
        print(strategic_report)
        print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
