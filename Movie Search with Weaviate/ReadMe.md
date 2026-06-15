# Movie Search with Weaviate 

This mini-project demonstrates how to ingest data into a Weaviate cloud database, perform advanced semantic vector searches, and execute Retrieval-Augmented Generation (RAG) by bridging Weaviate Cloud with a locally running Ollama LLM instance.

## Architecture Overview

The system utilizes Weaviate Cloud to store movie vectors and handle semantic proximity queries. To generate natural language output without cloud LLM costs, a secure ngrok tunnel routes contextual payloads from Weaviate directly to a local Ollama server running `llama3`.

For the RAG component, the mini-project first runs a check on the user prompt to determine if it is malicious or not using a guardrail created with Ollama which prompts the LLM to determine whether or not the user prompt is malicious and proceeds to generate a tweet if the prompt is not malicious followed by calculating a safety score to determine if the LLM hallucinated the tweet or the result is indeed accurate. 

## Setup

1. Clone the repository locally. 

2. Create a Python virtual environment in the Movie Search with Weaviate directory:

```bash
/usr/local/bin/python3 -m venv venv
source venv/bin/activate
```
3. Create a weaviate cluster and obtain your API Key and REST Endpoint URL. 

4. Export the latter using: 
```bash
export WEAVIATE_URL='insert url here'
export WEAVIATE_API_KEY='insert API Key here'
```
5. Install weaviate:
```bash
pip install -U "weaviate-client[agents]"
```
6. Install ollama:

https://ollama.com/download/mac

Because your Weaviate instance lives in the cloud, you must expose your local Ollama port to accept inbound external traffic. Open a terminal window and serve Ollama bound to all hosts:

7. Open Ollama and run: 

```bash
OLLAMA_HOST=0.0.0.0 /Applications/Ollama.app/Contents/Resources/ollama serve
```

8. Open a secure tunnel with ngrok:

```
ngrok http 11434
```

9. Copy the Forwarding URL from the terminal into the `NGROK_OLLAMA_ENDPOINT` variable in `retrieval_augmented_generation.py`.

To vectorize the data and create a new collection in Weaviate run:

```bash
python import_data.py
```

To run the search query for semantic searching similar movies run: 

```bash
python semantic_search.py
```

To generate a Tweet using Ollama and a movie from the Movie collection in Weaviate run: 

```bash
python retrieval_augmented_generation.py
```

10. To test the `retrieval_augmented_generation.py` script using the malicious prompt, replace `user_prompt` with `user_prompt_malicious` when calling the `get_scifi_movie` function.

## Built with: 
- Python
- Ollama (llama3)
- Weaviate vector database
- ngrok

## Sample Results:

- Running the semantic search using the query "Sci-fi" returns the following data:
  ```json
  {
    "genre": "Science Fiction",
    "description": "A computer hacker learns about the true nature of reality and his role in the war against its controllers.",
    "title": "The Matrix"
  }
  {
    "genre": "Fantasy",
    "description": "A meek Hobbit and his companions set out on a perilous journey to destroy a powerful ring and save Middle-earth.",
    "title": "The Lord of the Rings: The Fellowship of the Ring"
  }
  ```
- Running the query to generate a Tweet using Ollama and the Movie collection in Weaviate returns: 

  "Just watched #TheMatrix 🤖🔥 and I'm blown away by the mind-blowing action and thought-provoking themes! Whoa, Neo's awakening was EPIC 🚀 and I'm still reeling from the revelations about the simulated reality 😲 What's real, what's not? 🤯 Mind. Blown."

  ============================================================
📊 Initiating Native Faithfulness Audit Loop...
📋 Step A: Extracting explicit factual statements from generation...
🔎 Step B: Auditing 5 statement(s) against Weaviate Context ledger...
  ✅ [VALID]: The user watched The Matrix.
  ✅ [VALID]: The user is still reeling from the truth about the movie.
  ✅ [VALID]: The world isn't what it seems, according to the movie.
  ✅ [VALID]: Neo's journey in the movie is a wild ride.
  ✅ [VALID]: The user had their mind blown by something in the movie.
============================================================
🛡️ [Final Safety Score]: 100.0% Factual Accuracy
✅ Generation Approved: Factual accuracy verified against data cluster.
