from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def load_documents():
    all_docs = []

for pdf in Path("knowledge base").glob("*.pdf"):
  loader = PyPDFLoader(str(pdf))
  all_docs.extend(loader.load())

return all_docs
