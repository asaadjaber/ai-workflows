import os
import requests
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
import argparse

# 1. Initialize the same embedding engine you used for ingestion
embeddings = OllamaEmbeddings(model="nomic-embed-text")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Query your local codebase intelligence agent.")
    parser.add_argument(
        "--db", 
        type=str, 
        default="./moviepal_vector_db",  # Defaults to MoviePal if they don't provide one
        help="Path to the vector database directory"
    )
    return parser.parse_args()

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
    # 1. Load your existing codebase vector database
    args = parse_arguments()
    
    print(f"🗄️ Loading vector database from: {args.db}")
    vector_store = Chroma(
        persist_directory=args.db,  # Dynamic path loaded here!
        embedding_function=embeddings
    )

    # Initialize our running conversation history
    chat_history = []

    print("\n🚀 MoviePal Intelligence Agent is live!")
    print("Type your questions below. Type 'exit' or 'quit' to stop.\n")

    while True:
        # 2. Continuous user input loop
        query = input("👤 You: ")
        if query.strip().lower() in ['exit', 'quit']:
            print("👋 Exiting chat. Happy coding!")
            break
            
        if not query.strip():
            continue

        # 3. Context Retrieval
        # We still fetch the top 3 most relevant code snippets for the *current* query
        relevant_docs = vector_store.similarity_search(query, k=3)
        context_chunks = [doc.page_content for doc in relevant_docs]
        combined_context = "\n\n--- CODE SNIPPET ---\n\n".join(context_chunks)

        # 4. Format Chat History into a readable string for the model
        history_string = ""
        for turn in chat_history:
            history_string += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"

        # 5. Construct the Memory-Aware System Prompt
        final_prompt = f"""You are an expert software engineering assistant. 
            Use the following pieces of retrieved source code context and the conversation history to answer the user's question.

            --- CODE CONTEXT ---
            {combined_context}

            --- CONVERSATION HISTORY ---
            {history_string}

            Current User Question: {query}
            Answer:"""

        print("🤖 Thinking...")
        answer = query_local_ollama(final_prompt)
        
        print(f"\n🟢 Agent: {answer}\n")
        print("-" * 40)

        # 6. Append this entire interaction to our memory log
        chat_history.append({
            "user": query,
            "assistant": answer
        })    query = "Summarize the main architecture or view controllers found in this codebase."
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
