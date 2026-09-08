import os
import uuid

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# --------------------------------
# CONFIGURATION
# --------------------------------

CHROMA_PATH = "chroma_db_langchain"

EMBEDDING_MODEL = "embeddinggemma"


# --------------------------------
# EMBEDDINGS
# --------------------------------

embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL
)


# --------------------------------
# CREATE / LOAD VECTOR DATABASE
# --------------------------------

vector_db = Chroma(
    collection_name="study_material",
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)


# --------------------------------
# PDF TEXT SPLITTER
# --------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# --------------------------------
# ADD PDF TO DATABASE
# --------------------------------

def add_pdf_to_database(pdf_path):

    # Load PDF

    loader = PyPDFLoader(
        pdf_path
    )

    documents = loader.load()


    # Split into chunks

    chunks = text_splitter.split_documents(
        documents
    )


    # Add metadata

    for index, chunk in enumerate(chunks):

        chunk.metadata["source"] = os.path.basename(
            pdf_path
        )

        chunk.metadata["chunk"] = index


    # Create unique IDs

    ids = [

        str(uuid.uuid4())

        for _ in chunks

    ]


    # Add to ChromaDB

    vector_db.add_documents(
        documents=chunks,
        ids=ids
    )


    return len(chunks)


# --------------------------------
# SEARCH DOCUMENTS
# --------------------------------

def search_documents(
    query,
    k=4
):

    # Retrieve more candidates first
    results = vector_db.similarity_search_with_score(
        query,
        k=6
    )

    context = ""
    sources = set()

    # Keep only reasonably relevant results
    for document, score in results:

        # Chroma distance:
        # lower score = more similar
        if score > 1.2:
            continue

        context += (
            document.page_content
            + "\n\n"
        )

        source = document.metadata.get(
            "source"
        )

        if source:
            sources.add(source)

    return context, list(sources)