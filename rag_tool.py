from langchain_core.tools import tool

from langchain_rag import search_documents


@tool
def rag_search_tool(query: str) -> str:
    """
    Search the student's uploaded PDF study material.

    Use this tool when the student asks a question about
    information that may be present in their uploaded
    study notes or PDFs.

    Returns relevant information from the student's
    uploaded study material.
    """

    try:
        context, sources = search_documents(
            query,
            k=4
        )

        if not context.strip():
            return (
                "No relevant information was found "
                "in the uploaded study material."
            )

        result = "RELEVANT STUDY MATERIAL:\n\n"
        result += context

        if sources:
            result += "\n\nSOURCES:\n"
            result += "\n".join(sources)

        return result

    except Exception as e:
        return f"RAG search failed: {e}"