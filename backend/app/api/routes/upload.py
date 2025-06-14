"""
upload.py

This module handles the upload and processing of documents through a POST endpoint.

The uploaded file is:
- Parsed using OCR and/or text extraction
- Split into text chunks
- Stored in a persistent vector database with corresponding sentence embeddings

Route:
- POST / : Accepts a document file and returns the number of chunks successfully stored.

"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.ocr_service import extract_text_from_file
from app.services.vector_store import store_text_chunks

upload_router = APIRouter()

@upload_router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads and processes a document by extracting, chunking, and embedding its content.

    This endpoint supports PDF, image, and text files. It performs:
    - Text extraction via OCR or native PDF decoding
    - Paragraph-based chunking
    - Embedding generation using a sentence transformer
    - Storage of embeddings and metadata in ChromaDB

    Args:
        file (UploadFile): A file object sent via multipart/form-data

    Returns:
        dict: Response indicating upload status and number of stored text chunks

    Raises:
        HTTP 500: If any error occurs during file processing or storage
    """
    try:
        # Step 1: Extract and chunk text from uploaded file
        text_chunks = extract_text_from_file(file)

        # Step 2: Store the chunks in the vector store
        store_text_chunks(text_chunks)

        # Return the success response
        return {
            "status": "uploaded",
            "chunks": len(text_chunks)
        }

    except Exception as ex:
        # Handle and return error in JSON format
        return JSONResponse(
            status_code=500,
            content={
                "error": f"An error occurred while processing the uploaded document: {str(ex)}"
            }
        )
