"""
ocr_service.py

This module provides functionality to extract and chunk text from uploaded files.
Supported formats include:
- PDF (with selectable text and image-based OCR fallback)
- PNG, JPG, JPEG (image-based OCR using Tesseract)
- Plain text (.txt) files

Dependencies:
- pytesseract
- pdf2image
- PyPDF2
- typing

"""

import pytesseract
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from typing import List


def extract_text_from_file(file) -> List[dict]:
    """
    Extracts and chunks text from a supported uploaded file.

    This function supports various file formats:
    - PDF files: Attempts direct text extraction using PyPDF2,
                 with fallback to image-based OCR using pdf2image and pytesseract.
    - Image files (PNG, JPG, JPEG): Extracts text using Tesseract OCR.
    - Plain text files (.txt): Decodes and splits text directly.

    Args:
        file (UploadFile): File object from FastAPI file upload.

    Returns:
        List[dict]: A list of dictionaries with:
            - 'content' (str): Extracted chunk of text.
            - 'meta' (dict): Metadata including 'source'.
            If an error occurs during processing, a single dictionary with the
            error message is returned.
    """
    try:
        contents = file.file.read()
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            try:
                # Try extracting selectable text from the PDF
                file.file.seek(0)
                reader = PdfReader(file.file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

                # Fallback to OCR if no text found
                if not text.strip():
                    images = convert_from_bytes(contents)
                    text = "\n".join([pytesseract.image_to_string(img) for img in images])

            except Exception as pdf_error:
                return [{
                    "content": f"PDF processing failed: {str(pdf_error)}",
                    "meta": {"source": "upload"}
                }]

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            try:
                # Use OCR for image formats
                text = pytesseract.image_to_string(file.file)
            except Exception as img_error:
                return [{
                    "content": f"Image OCR failed: {str(img_error)}",
                    "meta": {"source": "upload"}
                }]

        else:
            try:
                # Decode plain text files
                text = contents.decode("utf-8")
            except Exception as decode_error:
                return [{
                    "content": f"Text decoding failed: {str(decode_error)}",
                    "meta": {"source": "upload"}
                }]

        return chunk_text(text)

    except Exception as general_error:
        return [{
            "content": f"File processing failed: {str(general_error)}",
            "meta": {"source": "upload"}
        }]


def chunk_text(text: str, max_tokens: int = 300) -> List[dict]:
    """
    Splits the input text into smaller chunks based on paragraph breaks.

    Note:
        Currently uses double newlines (`\n\n`) for splitting.
        Token-based chunking is not yet implemented.

    Args:
        text (str): The full text string to split into smaller parts.
        max_tokens (int): (Unused) Placeholder for future token-based logic.

    Returns:
        List[dict]: A list of chunk dictionaries with:
            - 'content': the individual paragraph text
            - 'meta': metadata about source
    """
    paragraphs = text.split("\n\n")
    return [
        {"content": p.strip(), "meta": {"source": "upload"}}
        for p in paragraphs if p.strip()
    ]
