import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_ingestion.tavily_scraper import extract_website_content
from data_ingestion.chunking import process_tavily_response
from data_ingestion.embedding import embed_chunks
from vector_store.qdrant_manager import setup_collection, upload_chunks
from query_system.retrieval import search_qdrant

def test_full_pipeline():
    url = "https://www.teikametrics.com/"
    print("Extracting website content...")
    response = extract_website_content(url)
    print("Cleaning and chunking...")
    chunks = process_tavily_response(response)
    print(f"Total chunks: {len(chunks)}")
    print("Generating embeddings...")
    chunks = embed_chunks(chunks)
    print("Setting up Qdrant collection...")
    setup_collection()
    print("Uploading chunks to Qdrant...")
    upload_chunks(chunks)
    print("Querying Qdrant...")
    query = "when was teikametrics founded"
    results = search_qdrant(query, top_k=3)
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
    test_full_pipeline()
