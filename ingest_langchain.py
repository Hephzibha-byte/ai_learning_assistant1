import os

from langchain_rag import add_pdf_to_database


DOCUMENTS_FOLDER = "documents"


def ingest_all_documents():

    if not os.path.exists(DOCUMENTS_FOLDER):

        print(
            "Documents folder not found!"
        )

        return


    pdf_files = [

        file

        for file in os.listdir(
            DOCUMENTS_FOLDER
        )

        if file.lower().endswith(
            ".pdf"
        )

    ]


    if not pdf_files:

        print(
            "No PDF files found in documents folder."
        )

        return


    for pdf_file in pdf_files:

        pdf_path = os.path.join(
            DOCUMENTS_FOLDER,
            pdf_file
        )


        print(
            f"\nProcessing: {pdf_file}"
        )


        chunks = add_pdf_to_database(
            pdf_path
        )


        print(
            f"Added {chunks} chunks."
        )


    print(
        "\nLangChain RAG database created successfully!"
    )


if __name__ == "__main__":

    ingest_all_documents()