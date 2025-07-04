import os
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API", "AIzaSyBrQKQJ-Ce_XvwAYLvAK2sdyzs744F1ZqQ")
EMBED_MODEL = "models/embedding-001"  # gemini-embedding-exp-03-07 alias

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API key not found.")

def embed_chunks(chunks: List[Dict[str, Any]], content_key: str = 'content') -> List[Dict[str, Any]]:
    """
    Generates embeddings for each chunk using Gemini embedding model.
    Adds the embedding to each chunk dict under 'embedding'.
    """
    texts = [chunk[content_key] for chunk in chunks]
    embeddings = []
    for text in texts:
        response = genai.embed_content(model=EMBED_MODEL, content=text, task_type="retrieval_document")
        embeddings.append(response['embedding'])
    for chunk, emb in zip(chunks, embeddings):
        chunk['embedding'] = emb
    return chunks
