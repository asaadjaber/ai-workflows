import os
import weaviate
from weaviate.classes.generate import GenerativeConfig

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

NGROK_OLLAMA_ENDPOINT = "***.ngrok-free.dev"

# Step 2.1: Connect to your Weaviate Cloud instance
with weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=weaviate_api_key
) as client:

    # Step 2.2: Use this collection
    movies = client.collections.use("Movie")

    # Step 2.3: Perform RAG with on NearText results
    response = movies.generate.near_text(
        query="sci-fi",
        limit=1,
        grouped_task="Write a tweet with emojis about this movie.",
        generative_provider=GenerativeConfig.ollama(
             api_endpoint=NGROK_OLLAMA_ENDPOINT,  # ◄── Weaviate Cloud can now route here!
             model="llama3" 
        )  # Configure the Anthropic generative integration for RAG
    )

    print(response.generative.text)  # Inspect the results
