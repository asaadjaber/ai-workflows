def retrieve_documents(
    vectorstore,
    question,
    k=3
):

return vectorstore.similarity_search(
    question,
    k=k
)
