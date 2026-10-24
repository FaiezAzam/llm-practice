from qdrant_client import QdrantClient
from src.config import settings


client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key,
)

collections = client.get_collections()
print("Connected to Qdrant.")
print("Collections:", [c.name for c in collections.collections])