from langchain_rag import search_documents


query = "What is cloud computing?"


context, sources = search_documents(
    query
)


print("\n--- RETRIEVED CONTEXT ---\n")

print(context)


print("\n--- SOURCES ---\n")

print(sources)