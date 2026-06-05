from langchain_community.vectorstores import Chroma

def build_vector_store(chunks, embeddings):

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

return vectorstore
