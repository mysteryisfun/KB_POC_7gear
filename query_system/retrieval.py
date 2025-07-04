import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Dict, Any

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API", "AIzaSyBrQKQJ-Ce_XvwAYLvAK2sdyzs744F1ZqQ")
QDRANT_API_KEY = os.getenv("QDRANT_API", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.fhsWdYnSxL79g1wQaGi4ZgFqile0ltlDwILjm5a4C1c")
QDRANT_URL = os.getenv("QDRANT_URL", "https://your-qdrant-instance.cloud.qdrant.io")
COLLECTION_NAME = "web_kb_chunks"
EMBED_MODEL = "models/embedding-001"  # gemini-embedding-exp-03-07 alias

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API key not found.")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def embed_query(query: str) -> List[float]:
    response = genai.embed_content(model=EMBED_MODEL, content=query, task_type="retrieval_query")
    return response['embedding']

def search_qdrant(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    query_vector = embed_query(query)
    hits = client.search(collection_name=COLLECTION_NAME, query_vector=query_vector, limit=top_k)
    return [hit.payload for hit in hits]
