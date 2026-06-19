# Local Codebase Intelligence Agent

This Retrieval-Augmented Generation (RAG) pipeline retrieves Swift and Python code files from a specified code base, chunks the files using recursive chunking, creates vector embeddings in ChromaDB using nomic-embed-text and generates an answer based on a query about the codebase's architectuer using Ollama (llama 3) completely offline.

## Built With: 
- Python 3
- LangChain (Recursive Character Text Splitter)
- ChromaDB (Local Vector Storage via `langchain-chroma`)
- Ollama (`llama3` and `nomic-embed-text`)
- Python `requests` (Direct Local API Orchestration)

## Set-up: 

1. Clone the repository locally.

2. Ensure you have Ollama installed on your desktop/PC and open in the background:
   
   `https://ollama.com/download/mac.`
   
3. Set up Python environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install langchain langchain-community langchain-chroma requests
   ```

5. Run the files ensuring the `target_dir` property in `ingest.py` points to your local code repository:
   ```bash
   python ingest.py
   python query_agent.py
   ```

## Sample Output: 

Based on the provided source code context, I can summarize the main architecture and view controllers as follows:

1. **ProfileViewController**: This is the main view controller responsible for managing a profile-related user interface (UI). It contains a UICollectionView and handles selection events.

2. **VibeDetailViewController**: This is a child view controller that is presented when an item in the collectionView is selected. Its purpose is unclear without more context, but it appears to be used to display details about a specific log (perhaps a video).

3. **HomeFeedViewController** (or its subclasses): These are two instances of a feed-related view controller. They are used as pages in the UIPageViewController and manage their own scrolling state.

4. **UIPageViewController**: This is the main page-based view controller that allows users to swipe between the HomeFeedViewControllers.

The architecture seems to be focused on managing multiple views and view controllers, with ProfileViewController acting as a hub for handling profile-related tasks and VibeDetailViewController serving as a detail-focused child view controller.
   
