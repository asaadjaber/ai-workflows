from load_documents import load_documents
from chunk_documents import chunk_documents
from create_embeddings import create_embeddings
from build_vector_store import build_vector_store
from retrieve import retrieve_documents

documents = load_documents()

print(f"Loaded {len(documents)} pages")

chunks = chunk_documents(documents)

print(f"Created {len(chunks)} chunks")

embeddings = create_embeddings()

vectorstore = build_vector_store(
    chunks,
    embeddings
)

question = "What companies have I worked for?"

results = retrieve_documents(
    vectorstore,
    question
)

for result in results:
    print("\n---")
    print(result.metadata)
    print(result.page_content)
