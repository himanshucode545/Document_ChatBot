"""
theme_summarizer.py

This module provides functionality to summarize themes from a list of document chunks
using Hugging Face's summarization pipeline (BART-Large-CNN model).

Dependencies:
- transformers
- typing

"""

from transformers.pipelines import pipeline
from typing import List, Dict

# Initialize the summarization pipeline using a pre-trained BART model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_themes(chunks: List[Dict[str, str]]) -> str:
    """
    Summarizes common themes from a list of document chunks.

    This function takes in multiple document segments (chunks), concatenates their content,
    and splits it into smaller pieces if needed to fit model input limits. Each piece is summarized
    and combined to form an overall thematic summary.

    Args:
        chunks (List[Dict[str, str]]): A list of dictionaries where each dict contains:
            - 'content' (str): The textual content of the chunk.
            - 'meta' (dict, optional): Metadata related to the chunk (not used here).

    Returns:
        str: A coherent summary string derived from all provided text chunks,
             or an error message if summarization fails.
    """
    try:
        # Join all valid text chunks into a single string
        texts = "\n".join([c['content'] for c in chunks if 'content' in c])

        if not texts.strip():
            return "No valid content found to summarize."

        # Define max characters per chunk (fits model input size ~512 tokens)
        max_chunk_chars = 1000
        text_parts = [texts[i:i + max_chunk_chars] for i in range(0, len(texts), max_chunk_chars)]

        summaries = []
        for part in text_parts:
            input_len = len(part.split())

            # Dynamically set max_length for summarization (based on input length)
            max_len = max(30, min(150, int(input_len * 0.7)))

            # Generate summary using the transformer model
            summary = summarizer(part, max_length=max_len, min_length=20, do_sample=False)

            # Extract summary text from the pipeline response
            summaries.append(summary[0]['summary_text'])  # type: ignore

        # Combine all partial summaries into one final summary
        return "\n".join(summaries)

    except Exception as e:
        return f"Summarization failed: {str(e)}"
