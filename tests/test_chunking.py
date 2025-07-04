import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_ingestion.tavily_scraper import extract_website_content
from data_ingestion.chunking import process_tavily_response

def test_clean_and_chunk():
    url = "https://www.teikametrics.com/"
    response = extract_website_content(url)
    chunks = process_tavily_response(response)
    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks for brevity
        print(f"\nChunk {i+1} metadata:")
        for k, v in chunk.items():
            if k == 'content':
                print(f"{k}: {v[:200]}...")  # Print first 200 chars
            else:
                print(f"{k}: {v}")

if __name__ == "__main__":
    test_clean_and_chunk()
