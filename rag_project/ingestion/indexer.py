import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams , PointStruct
from src.config import settings
from rag_project.ingestion.embedder import Embedder

COLLECTION_NAME = "html_tutorial"
VECTOR_SIZE = 384

def create_collection(client: QdrantClient) -> None:
        """Delete and recreate the collection with the correct vector config."""
        if client.collection_exists(COLLECTION_NAME):
                client.delete_collection(COLLECTION_NAME)

        client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )

def index_chunks(chunks: list[dict], embedder: Embedder, client: QdrantClient) -> None:
        """Embed chunks and upload them to Qdrant."""
        print(f"Embedding {len(chunks)} chunks....")

        # Get just the texts
        texts = [chunk['text'] for chunk in chunks]

        # Embed all at once
        vectors = embedder.embed(texts)

        # Build points
        points = [
                PointStruct(
                        id=chunk["chunk_index"],
                        vector=vector,
                        payload={
                                "text":chunk["text"],
                                "source":chunk["source"],
                                "page":chunk["page"]
                        },
                )
                for chunk,vector in zip(chunks,vectors)
        ]

        print(f"Uploading {len(points)} points to Qdrant...")
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print("Upload complete")

if __name__ == "__main__":
        with open("rag_project/data/chunks.json") as f:
                chunks = json.load(f)
        print(f"Loaded {len(chunks)} chunks")

        client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

        create_collection(client)
        print(f"Collection '{COLLECTION_NAME}' created")

        embedder = Embedder()

        index_chunks(chunks, embedder, client)

        count = client.count(COLLECTION_NAME).count
        print(f"Collection '{COLLECTION_NAME}' now has {count} points")
