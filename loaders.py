from langchain_community.document_loaders import PyPDFLoader
import os
import zipfile
import tempfile
from typing import List

def load_pdf_text(pdf_path: str) -> str:
    """Load text from a single PDF using LangChain PyPDFLoader"""
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])

def extract_zip_to_temp(uploaded_zip) -> str:
    """Extract uploaded ZIP to a temporary directory"""
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "uploaded.zip")
    with open(zip_path, "wb") as f:
        f.write(uploaded_zip.read())
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir

def get_pdf_files_from_dir(folder_path: str) -> List[str]:
    """Return sorted list of PDF file paths in folder"""
    return sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".pdf")])
