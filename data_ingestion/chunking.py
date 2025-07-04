import re
from typing import List, Dict, Any
from datetime import datetime

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing excessive whitespace, HTML tags, and unwanted boilerplate/navigation/footer content.
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove common navigation/footer/boilerplate phrases
    boilerplate_patterns = [
        r'(?i)home(\s*\|\s*)?',
        r'about( us)?(\s*\|\s*)?',
        r'contact( us)?(\s*\|\s*)?',
        r'privacy policy(\s*\|\s*)?',
        r'terms( &| and)? conditions(\s*\|\s*)?',
        r'login(\s*\|\s*)?',
        r'copyright.*?\d{4}',
        r'\bmenu\b',
        r'\bquick links?\b',
        r'\bsubscribe\b',
        r'\bnewsletter\b',
        r'\bcareers?\b',
        r'\bfaq\b',
        r'\bback arrow\b',
        r'\bnext arrow\b',
        r'\bget direction\b',
        r'\baddress\b',
        r'\bcontact\b',
        r'\bteam image\b',
        r'\bsee .*? in action\b',
        r'\bbook of business overview\b',
        r'\bupdated [a-z]{3,9} \d{1,2}, \d{4}\b',
        r'\bpromoters?\b',
        r'\bclient interactions?\b',
        r'\bscore\b',
        r'\b0\b',
        r'\bconversations? are happening\b',
        r'\bquick link\b',
        r'\bplug in\b',
        r'\bpower up\b',
        r'\bget intelligence\b',
        r'\bteam image \d+\b',
        r'\bsee [^\n]+ in action\b',
        r'\bget ready to accelerate your growth\b',
        r'\bsee 7th gear in action\b',
        r'\bclient health status\b',
        r'\bframerusercontent.com[^\s]*',
        r'\bapp.7thgear.ai[^\s]*',
        r'\bsupport@7thgear.ai\b',
        r'\b212th PL SE, Bothell, WA 98021, USA\b',
        r'\b\+1 425 445 4063\b',
        r'\bhello@7thgear.ai\b',
        r'\bcallto:[^\s]+',
        r'\bmailto:[^\s]+',
        r'\bterms of service\b',
        r'\bmaster subscription agreement\b',
        r'\bmsa\b',
        r'\bprivacy\b',
        r'\bterms\b',
        r'\bpolicy\b',
        r'\baddress\b',
        r'\bcontact\b',
        r'\bteam\b',
        r'\babout\b',
        r'\bhome\b',
        r'\bfeatures\b',
        r'\bbenefits\b',
        r'\bsubscribe\b',
        r'\bnewsletter\b',
        r'\bfaq\b',
        r'\bcareers?\b',
        r'\bterms & conditions\b',
        r'\bprivacy policy\b',
        r'\bterms of service\b',
        r'\bcontact us\b',
        r'\babout us\b',
        r'\bhome\b',
        r'\bfeatures\b',
        r'\bbenefits\b',
        r'\bteam\b',
        r'\bscore\b',
        r'\bupdated\b',
        r'\bpromoters\b',
        r'\bclient interactions\b',
        r'\bbook of business overview\b',
        r'\bconversations are happening\b',
        r'\bquick link\b',
        r'\bplug in\b',
        r'\bpower up\b',
        r'\bget intelligence\b',
        r'\bteam image\b',
        r'\bsee .*? in action\b',
        r'\bget ready to accelerate your growth\b',
        r'\bsee 7th gear in action\b',
        r'\bclient health status\b',
        r'\bframerusercontent.com[^\s]*',
        r'\bapp.7thgear.ai[^\s]*',
        r'\bsupport@7thgear.ai\b',
        r'\b212th PL SE, Bothell, WA 98021, USA\b',
        r'\b\+1 425 445 4063\b',
        r'\bhello@7thgear.ai\b',
        r'\bcallto:[^\s]+',
        r'\bmailto:[^\s]+',
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    # Replace multiple newlines and spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text: str, max_tokens: int = 500, overlap: int = 100, max_bytes: int = 30000) -> List[str]:
    """
    Splits text into chunks of approximately max_tokens words, with overlap for context.
    Ensures no chunk exceeds max_bytes (for embedding API safety).
    Tries to split on paragraph boundaries if possible.
    """
    # Try to split by paragraphs first
    paragraphs = [p.strip() for p in re.split(r'\n{2,}|\r{2,}', text) if p.strip()]
    chunks = []
    current_chunk = []
    current_len = 0
    for para in paragraphs:
        words = para.split()
        if current_len + len(words) > max_tokens and current_chunk:
            chunk = ' '.join(current_chunk)
            if len(chunk.encode('utf-8')) <= max_bytes:
                chunks.append(chunk)
            else:
                # If chunk is too large, split further by sentences
                sentences = re.split(r'(?<=[.!?]) +', chunk)
                temp = []
                for sent in sentences:
                    temp.append(sent)
                    temp_chunk = ' '.join(temp)
                    if len(temp_chunk.encode('utf-8')) > max_bytes:
                        # Remove last, add chunk, start new
                        temp.pop()
                        chunks.append(' '.join(temp))
                        temp = [sent]
                if temp:
                    chunks.append(' '.join(temp))
            # Overlap
            if overlap > 0:
                overlap_words = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                current_chunk = list(overlap_words)
                current_len = len(current_chunk)
            else:
                current_chunk = []
                current_len = 0
        current_chunk.extend(words)
        current_len += len(words)
    if current_chunk:
        chunk = ' '.join(current_chunk)
        if len(chunk.encode('utf-8')) <= max_bytes:
            chunks.append(chunk)
        else:
            sentences = re.split(r'(?<=[.!?]) +', chunk)
            temp = []
            for sent in sentences:
                temp.append(sent)
                temp_chunk = ' '.join(temp)
                if len(temp_chunk.encode('utf-8')) > max_bytes:
                    temp.pop()
                    chunks.append(' '.join(temp))
                    temp = [sent]
            if temp:
                chunks.append(' '.join(temp))
    return [c for c in chunks if len(c.split()) > 30]


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
