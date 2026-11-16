import pymupdf

from backend.app.services.text_cleaner import clean_text
from backend.app.services.section_parser import parse_sections


def extract_text_from_pdf(file_path: str) -> str:
    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return clean_text(text)


def extract_resume_sections(file_path: str):
    text = extract_text_from_pdf(file_path)

    return parse_sections(text)