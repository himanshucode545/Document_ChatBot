import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "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")
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "./chroma_db")

settings = Settings()
