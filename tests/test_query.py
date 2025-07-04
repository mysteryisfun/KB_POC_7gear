import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_store.supabase_manager import search_supabase
from data_ingestion.embedding import embed_chunks

def test_query():
    query = input("Enter your query: ")
    top_k = int(input("How many top results? (default 3): ") or 3)
    # Embed the query using Gemini
    from data_ingestion.embedding import GEMINI_API_KEY, EMBED_MODEL
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        raise ValueError("GEMINI_API key not found.")
    response = genai.embed_content(model=EMBED_MODEL, content=query, task_type="retrieval_query")
    query_embedding = response['embedding']
    results = search_supabase(query_embedding, top_k=top_k)
    print(f"\nTop results for query: '{query}'\n")
    for i, res in enumerate(results):
        print(f"Result {i+1}:")
        for k, v in res.items():
            if k == 'content':
                print(f"{k}: {v[:200]}...")
            else:
                print(f"{k}: {v}")
        print()

if __name__ == "__main__":
    test_query()
