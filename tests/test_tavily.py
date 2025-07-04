import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_ingestion.tavily_scraper import extract_website_content


def test_extract_website_content():
    url = "https://www.7thgear.ai/"
    result = extract_website_content(url)
    print(result)


if __name__ == "__main__":
    test_extract_website_content()