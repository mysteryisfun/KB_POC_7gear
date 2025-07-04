import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List, Dict, Any
import uuid

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL", "<your-supabase-url>")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<your-supabase-service-role-key>")
TABLE_NAME = "web_kb_chunks"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_chunks_supabase(chunks: List[Dict[str, Any]]):
    for chunk in chunks:
        chunk_id = str(uuid.uuid4())
        embedding = chunk['embedding']
        payload = {
            "id": chunk_id,
            "embedding": embedding,
            "content": chunk['content'],
            "source_url": chunk['source_url'],
            "chunk_meta": chunk.get('title', ''),
            "date_published": chunk.get('date_published', ''),
        }
        supabase.table(TABLE_NAME).insert(payload).execute()

def search_supabase(query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
    # This assumes you have the pgvector extension enabled and a vector column named 'embedding'
    sql = f"""
        select *, (1 - (embedding <#> '{query_embedding}'::vector)) as score
        from {TABLE_NAME}
        order by score desc
        limit {top_k};
    """
    result = supabase.rpc('execute_sql', {"sql": sql}).execute()
    return result.data if hasattr(result, 'data') else result
