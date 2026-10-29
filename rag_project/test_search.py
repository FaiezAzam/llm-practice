from qdrant_client import QdrantClient
from src.config import settings
from rag_project.ingestion.embedder import Embedder


client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
embedder = Embedder()

query = "How do you create a line break in HTML?"
query_vector = embedder.embed([query])[0]

results = client.query_points(
    collection_name="html_tutorial",
    query=query_vector,
    limit=3,
)

for hit in results.points:
    print(f"Score: {hit.score:.4f}")
    print(f"Source: {hit.payload['source']}, Page: {hit.payload['page']}")
    print(f"Text: {hit.payload['text'][:250]}...")
    print("---")