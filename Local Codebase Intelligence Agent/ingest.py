import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

def load_local_code_files(directory_path):
    """
    Traverses a local directory and reads files.
    This reinforces your previous file I/O skills!
    """
    raw_documents = []
    
    for root, dirs, files in os.walk(directory_path):
        # Defensive check: skip hidden directories like .git or .DS_Store
        if any(hidden in root for hidden in [".git", "__pycache__", "storage"]):
            continue
            
        for file in files:
            # We only want to read Python or Swift files for this test
            if file.endswith(('.py', '.swift')) and not file.startswith('.'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Wrap the raw text in a LangChain Document object
                        doc = Document(
                            page_content=content,
                            metadata={"source": file_path, "filename": file}
                        )
                        raw_documents.append(doc)
                except Exception as e:
                    print(f"Skipping corrupt or unreadable file {file}: {e}")
                    
    return raw_documents

# --- Test execution stub ---
if __name__ == "__main__":
    # Let's target the directory where your recent python router files are kept!
    target_dir = "/Users/asaadjaber/MoviePal"

    chroma_db_dir = "./moviepal_vector_db"

    if not os.path.exists(target_dir):
        print(f"❌ Error: The directory '{target_dir}' was not found. Please verify the path.")
    else:
        print("🔍 Scanning directory for source code files...")
        docs = load_local_code_files(target_dir)
        print(f"✅ Successfully loaded {len(docs)} source files.")

        # --- NEW: CHUNKING LOGIC ---
        print("✂️ Splitting documents into logical code chunks...")
        
        # We tell the splitter to make chunks of ~1000 characters, with a 200 character overlap
        # so code context isn't lost right at the split line.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        
        # Split our raw files into a list of smaller chunked Document objects
        chunked_docs = text_splitter.split_documents(docs)
        print(f"📦 Created {len(chunked_docs)} distinct text chunks from your codebase.")

        # --- NEW: VECTORIZATION & STORAGE ---
        print("🧬 Initializing local Ollama embedding engine...")
        # Tell LangChain to use your local mapmaker model
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        print("💾 Calculating coordinates and writing to local database (Chroma)...")
        # This takes the text chunks, embeds them, and saves the database files to disk
        vector_store = Chroma.from_documents(
            documents=chunked_docs,
            embedding=embeddings,
            persist_directory=chroma_db_dir
        )
        
        print(f"🚀 Success! Your codebase vector database is stored locally at: {chroma_db_dir}")
