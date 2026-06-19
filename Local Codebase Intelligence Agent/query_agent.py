import os
import requests
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

# 1. Initialize the same embedding engine you used for ingestion
embeddings = OllamaEmbeddings(model="nomic-embed-text")

def query_local_ollama(prompt):
    """
    Sends a direct HTTP request to your local Ollama instance.
    This replaces the unreliable LangChain LLM wrapper!
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False  # Gives us the full answer at once
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response text found.")
    except Exception as e:
        return f"❌ Failed to connect to Ollama: {e}. Is the Ollama app running?"

if __name__ == "__main__":
    # 2. Load your existing codebase vector database
    print("🗄️ Loading MoviePal vector database...")
    vector_store = Chroma(
        persist_directory="./moviepal_vector_db",
        embedding_function=embeddings
    )

    # 3. Ask your question
    query = "Summarize the main architecture or view controllers found in this codebase."
    print(f"🤔 Querying MoviePal database for: '{query}'...\n")

    # 4. Fetch the top 3 most relevant code snippets manually
    relevant_docs = vector_store.similarity_search(query, k=3)
    
    # Extract and combine the raw code text from the retrieved documents
    context_chunks = [doc.page_content for doc in relevant_docs]
    combined_context = "\n\n--- CODE SNIPPET ---\n\n".join(context_chunks)

    # 5. Construct a clean system prompt mapping context to the question
    final_prompt = f"""You are an expert software engineering assistant. 
        Use the following pieces of retrieved source code context to answer the user's question. 
        If you don't know the answer based on the code, say that you don't know.

        Context:
        {combined_context}

        User Question: {query}
        Answer:"""

    print("🤖 Sending relevant code context to Llama 3...")
    answer = query_local_ollama(final_prompt)
    
    print("\n🟢 Agent Response:")
    print(answer)
