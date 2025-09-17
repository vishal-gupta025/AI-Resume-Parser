import streamlit as st
import tempfile
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file.")

from loaders import load_pdf_text, extract_zip_to_temp, get_pdf_files_from_dir
from parsers import str_parser, pydantic_parser, llm_resume_parser
from utils import save_json

st.title("📄 AI Resume Parser")
st.write("Upload a ZIP folder or single PDF containing resumes. Get structured JSON output.")

uploaded_file = st.file_uploader("Upload ZIP or single PDF", type=["zip","pdf"])

parser_choice = st.selectbox(
    "Choose a parser",
    ["StrOutputParser (Raw Text)", "PydanticOutputParser (Direct Schema)", "LLMResumeParser (Recommended)"]
)

if uploaded_file and st.button("Parse Resumes"):
    results = []

    # Determine PDFs to process
    if uploaded_file.type == "application/zip":
        folder_path = extract_zip_to_temp(uploaded_file)
        pdf_files = get_pdf_files_from_dir(folder_path)
    elif uploaded_file.type == "application/pdf":
        temp_dir = tempfile.mkdtemp()
        pdf_path = os.path.join(temp_dir, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        pdf_files = [pdf_path]
    else:
        st.error("Unsupported file type!")
        st.stop()

    # Process PDFs in sequence
    for pdf_file in pdf_files:
        text = load_pdf_text(pdf_file)

        if parser_choice == "StrOutputParser (Raw Text)":
            parsed = str_parser.parse(text)
        elif parser_choice == "PydanticOutputParser (Direct Schema)":
            parsed = pydantic_parser.parse(text)
        elif parser_choice == "LLMResumeParser (Recommended)":
            parsed = llm_resume_parser.parse(text)

        results.append({
            "file": os.path.basename(pdf_file),
            "parsed": parsed
        })

    # Display results
    st.json(results)

    # Save JSON for download
    json_path = save_json(results)
    st.download_button(
        label="⬇️ Download Parsed JSON",
        data=open(json_path, "rb"),
        file_name="parsed_resumes.json",
        mime="application/json"
    )
