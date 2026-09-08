import os

from rag import add_pdf_to_database


DOCUMENT_FOLDER = "documents"


def ingest_all_documents():

    files = os.listdir(DOCUMENT_FOLDER)

    pdf_files = [
        file
        for file in files
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:

        print("No PDF files found.")

        return

    for pdf_file in pdf_files:

        path = os.path.join(
            DOCUMENT_FOLDER,
            pdf_file
        )

        print(f"Processing: {pdf_file}")

        chunks = add_pdf_to_database(path)

        print(
            f"Added {chunks} chunks."
        )

    print("\nRAG database created successfully!")


if __name__ == "__main__":

    ingest_all_documents()