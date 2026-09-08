from rag_tool import rag_search_tool


print("\n========================================")
print("TEST — RAG LANGCHAIN TOOL")
print("========================================\n")


question = "What is cloud computing?"


print("Question:")
print(question)


print("\nSearching uploaded study material...\n")


result = rag_search_tool.invoke(
    {
        "query": question
    }
)


print("RAG TOOL RESULT:")
print("----------------------------------------")
print(result)