import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="docs")
model = SentenceTransformer("all-MiniLM-L6-v2")

def store_text_chunks(chunks):
    """
    Stores text chunks in ChromaDB with their sentence embeddings.

    Args:
        chunks (list): A list of dictionaries with keys:
            - 'content': str, the text content of the chunk.
            - 'meta': dict, must include 'source': full filename.

    Returns:
        dict: Status of storage
    """
    try:
        current_size = len(collection.get()['ids'])

        for i, chunk in enumerate(chunks):
            embedding = model.encode(chunk['content']).tolist()
            collection.add(
                documents=[chunk['content']],
                metadatas=[chunk['meta']],
                ids=[f"chunk_{current_size + i}"],
                embeddings=[embedding]
            )

        return {"status": "success", "message": f"{len(chunks)} chunks stored."}

    except Exception as e:
        return {"status": "error", "message": f"Failed to store chunks: {str(e)}"}

def search_similar(query, k=5):
    """
    Searches for the top-k similar documents in ChromaDB using sentence embeddings.

    Args:
        query (str): The input query text.
        k (int): Number of top results to return

    Returns:
        list: List of matched chunks with document name included
    """
    try:
        q_emb = model.encode(query).tolist()
        results = collection.query(query_embeddings=[q_emb], n_results=k)

        documents = results["documents"][0] # type: ignore
        metadatas = results["metadatas"][0] # type: ignore

        return [
            {
                "content": doc,
                "meta": {
                    "source": meta.get("source", "unknown")  # Safely extract filename
                }
            }
            for doc, meta in zip(documents, metadatas)
        ]

    except Exception as e:
        return {"status": "error", "message": f"Search failed: {str(e)}"}
