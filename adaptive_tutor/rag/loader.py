from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


def load_documents(folder_path):
    """
    Load curriculum PDFs.
    """

    documents = []

    folder = Path(folder_path)

    if not folder.exists():
        return documents

    for pdf in folder.glob("*.pdf"):

        try:
            loader = PyPDFLoader(str(pdf))

            documents.extend(
                loader.load()
            )

        except Exception as e:

            print(
                f"Failed loading {pdf}: {e}"
            )

    return documents


# =====================================================
# Question Bank Loader
# =====================================================

def load_question_bank(file_path):
    """
    Load previously generated questions.

    Format:
    One question per line.
    """

    path = Path(file_path)

    if not path.exists():
        return []

    documents = []

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                question = line.strip()

                if not question:
                    continue

                documents.append(
                    Document(
                        page_content=question,
                        metadata={
                            "source": "question_bank"
                        }
                    )
                )

    except Exception as e:

        print(
            f"Question bank load failed: {e}"
        )

    return documents


# =====================================================
# Merge Multiple Sources
# =====================================================

def load_all_documents(
    curriculum_folder,
    question_bank_file=None,
):
    """
    Curriculum PDFs +
    Stored Questions
    """

    docs = load_documents(
        curriculum_folder
    )

    if question_bank_file:

        docs.extend(
            load_question_bank(
                question_bank_file
            )
        )

    return docs