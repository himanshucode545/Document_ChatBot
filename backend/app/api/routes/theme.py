"""
theme.py

This module defines an API route for extracting and summarizing thematic insights 
from document embeddings using semantic search and abstractive summarization.

Routes:
- GET / : Accepts a query string `q`, retrieves top relevant document chunks using 
  vector search, and summarizes the collective themes using a transformer model.

"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.services.vector_store import search_similar
from app.services.synthesis import summarize_themes
from typing import Dict, Any

theme_router = APIRouter()

@theme_router.get("/", response_model=Dict[str, Any])
def summarize_question(q: str = Query(..., description="The user query for which thematic summarization is needed")):
    """
    Endpoint to summarize themes from document chunks most relevant to a user query.

    This function:
    - Uses vector-based semantic search to find relevant chunks from documents
    - Applies an abstractive summarizer to extract a coherent summary of recurring themes

    Args:
        q (str): The user’s query string.

    Returns:
        dict: A JSON response containing:
            - 'question': the original query string
            - 'themes': a summarized version of the relevant document contents
    """
    try:
        # Step 1: Retrieve most relevant chunks
        answers = search_similar(q)

        # Step 2: Summarize the themes from the matched content
        summary = summarize_themes(answers)

        return {
            "question": q,
            "themes": summary
        }

    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"An error occurred while summarizing the themes: {str(ex)}"
            }
        )
