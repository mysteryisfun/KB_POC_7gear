import os
from tavily import TavilyClient
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)


def extract_website_content(url: str) -> dict:
    """
    Extracts website content using Tavily API.
    Args:
        url (str): The target website URL.
    Returns:
        dict: The response from Tavily API containing the website content in plain text format.
    """
    if not url or not url.startswith('http'):
        raise ValueError("A valid URL must be provided.")
    tavily_api_key = os.getenv("TAVILY_API_KEY","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")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables.")
    client = TavilyClient(tavily_api_key)
    response = client.crawl(url=url, format="text", language="en")
    return response


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tavily_scraper.py <url>")
        exit(1)
    url = sys.argv[1]
    result = extract_website_content(url)
    print(result)
