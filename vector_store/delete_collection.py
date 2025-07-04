import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

QDRANT_API_KEY = os.getenv("QDRANT_API", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.fhsWdYnSxL79g1wQaGi4ZgFqile0ltlDwILjm5a4C1c")
QDRANT_URL = os.getenv("QDRANT_URL", "https://your-qdrant-instance.cloud.qdrant.io")
COLLECTION_NAME = "web_kb_chunks"

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def delete_collection():
    if COLLECTION_NAME in [c.name for c in client.get_collections().collections]:
        client.delete_collection(collection_name=COLLECTION_NAME)
        print(f"Deleted collection: {COLLECTION_NAME}")
    else:
        print(f"Collection {COLLECTION_NAME} does not exist.")

if __name__ == "__main__":
    delete_collection()
