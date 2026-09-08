import os
import uuid

import chromadb
from pypdf import PdfReader
import ollama


# --------------------------------
# CHROMADB
# --------------------------------

CHROMA_PATH = "chroma_db"


chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = chroma_client.get_or_create_collection(
    name="study_material"
)


# --------------------------------
# EXTRACT TEXT FROM PDF
# --------------------------------

def extract_pdf_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# --------------------------------
# SPLIT TEXT INTO CHUNKS
# --------------------------------

def split_text(text, chunk_size=1000):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks


# --------------------------------
# CREATE LOCAL EMBEDDING
# --------------------------------

def create_embedding(text):

    response = ollama.embed(
        model="embeddinggemma",
        input=text
    )

    return response["embeddings"][0]


# --------------------------------
# ADD PDF TO CHROMADB
# --------------------------------

def add_pdf_to_database(pdf_path):

    text = extract_pdf_text(pdf_path)

    chunks = split_text(text)

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    filename = os.path.basename(pdf_path)

    for index, chunk in enumerate(chunks):

        embedding = create_embedding(chunk)

        ids.append(str(uuid.uuid4()))

        embeddings.append(embedding)

        documents.append(chunk)

        metadatas.append({
            "source": filename,
            "chunk": index
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    return len(chunks)


# --------------------------------
# SEARCH THE RAG DATABASE
# --------------------------------

def search_documents(query):

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=4
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    context = ""

    sources = set()

    for document, metadata in zip(
        documents,
        metadatas
    ):

        context += document + "\n\n"

        if metadata and "source" in metadata:

            sources.add(
                metadata["source"]
            )

    return context, list(sources)