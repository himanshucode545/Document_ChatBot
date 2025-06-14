"""
query_router.py

This module defines an API endpoint for processing user queries against document embeddings
stored in ChromaDB. It uses semantic search to find the most relevant document chunks 
related to a user's question using Sentence Transformers.

Routes:
- GET / : Accepts a query string `q` and returns the top-matching chunks of text along with metadata.

"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.services.vector_store import search_similar
from typing import Dict, Any

query_router = APIRouter()

@query_router.get("/", response_model=Dict[str, Any])
def ask_question(q: str = Query(..., description="The user query to search similar document chunks for")):
    """
    Endpoint to handle user queries and search for similar document chunks using sentence embeddings.

    Args:
        q (str): The query string submitted by the user.

    Returns:
        dict: A JSON response containing:
            - 'question': the original query string
            - 'answers': a list of top-matching document chunks with their content and metadata
    """
    try:
        # Perform semantic similarity search using vector embeddings
        results = search_similar(q)

        return {
            "question": q,
            "answers": results
        }

    except Exception as ex:
        # Return error details in case of failure
        return JSONResponse(
            status_code=500,
            content={
                "error": f"An error occurred while searching similar questions: {str(ex)}"
            }
        )
