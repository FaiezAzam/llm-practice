from rag_project.ingestion.embedder import Embedder
import numpy as np

embedder = Embedder()

text = [
    "What is the br tag?",
    "HTML is a markup language.",
    "The cat sat on the mat.",
]

vectors = embedder.embed(text)

print(f"Number of vectors: {len(vectors)}")
print(f"Dimension of first vector: {len(vectors[0])}")
print(f"First 5 numbers of first vector: {vectors[0][:5]}")
print(f"First 5 numbers of second vector: {vectors[1][:5]}")

def cosine_similarity(a,b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a,b) / np.linalg.norm(a) * np.linalg.norm(b))

print(f"Similarity (br tag vs HTML):  {cosine_similarity(vectors[0], vectors[1]):.4f}")
print(f"Similarity (br tag vs cat):   {cosine_similarity(vectors[0], vectors[2]):.4f}")
print(f"Similarity (HTML vs cat):     {cosine_similarity(vectors[1], vectors[2]):.4f}")