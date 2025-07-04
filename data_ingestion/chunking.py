import re
from typing import List, Dict, Any
from datetime import datetime

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing excessive whitespace, HTML tags, and unwanted characters.
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Replace multiple newlines and spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text: str, max_tokens: int = 800, overlap: int = 100) -> List[str]:
    """
    Splits text into chunks of approximately max_tokens words, with overlap for context.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_tokens, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start = end - overlap  # overlap for context
    return chunks


def process_tavily_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Processes Tavily API response, cleans and chunks content, and adds metadata.
    Returns a list of chunk dicts with metadata.
    """
    all_chunks = []
    base_url = response.get('base_url', '')
    results = response.get('results', [])
    for page in results:
        url = page.get('url', base_url)
        raw_content = page.get('raw_content', '')
        title = ''  # Tavily may not provide title; can be extracted if present
        date_published = datetime.utcnow().isoformat()
        clean_content = clean_text(raw_content)
        chunks = chunk_text(clean_content)
        for idx, chunk in enumerate(chunks):
            chunk_metadata = {
                'source_url': url,
                'chunk_id': f"{url}#chunk{idx+1}",
                'title': title,
                'date_published': date_published,
                'content': chunk
            }
            all_chunks.append(chunk_metadata)
    return all_chunks
