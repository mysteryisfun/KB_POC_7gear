import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
from typing import List, Dict, Any
import uuid

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

QDRANT_API_KEY = os.getenv("QDRANT_API", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.fhsWdYnSxL79g1wQaGi4ZgFqile0ltlDwILjm5a4C1c")
QDRANT_URL = os.getenv("QDRANT_URL", "https://d4a7ad5d-e5ed-4802-ba05-f9882ed7ea8d.eu-west-2-0.aws.cloud.qdrant.io")
COLLECTION_NAME = "web_kb_chunks"
VECTOR_SIZE = 768  # Gemini embedding size

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def setup_collection():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )

def upload_chunks(chunks: List[Dict[str, Any]]):
    points = []
    for idx, chunk in enumerate(chunks):
        # Use a UUID for point id to meet Qdrant requirements
        point_id = str(uuid.uuid4())
        points.append(PointStruct(
            id=point_id,
            vector=chunk['embedding'],
            payload={k: v for k, v in chunk.items() if k != 'embedding'}
        ))
    client.upsert(collection_name=COLLECTION_NAME, points=points)
