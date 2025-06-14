def chunk_text(text: str, max_tokens: int = 300):
    """
    Splits a large block of text into smaller paragraph-based chunks.

    Args:
        text (str): The raw extracted text to be chunked into manageable parts.
        max_tokens (int, optional): Placeholder for future token-based chunking. Currently unused.
                                    Default is 300.

    Returns:
        List[Dict[str, Dict[str, str]]]: A list of dictionaries where each dictionary contains:
            - 'content': A single paragraph of text.
            - 'meta': Metadata with a static source label ("upload").
    """
    # Split the text on double newlines, which usually separate paragraphs
    paragraphs = text.split("\n\n")

    # Create a list of dictionaries with cleaned paragraphs and metadata
    return [
        {
            "content": p.strip(),       # Clean leading/trailing spaces
            "meta": {"source": "upload"}
        }
        for p in paragraphs if p.strip()  # Exclude empty or whitespace-only paragraphs
    ]
