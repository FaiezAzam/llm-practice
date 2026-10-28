from sentence_transformers import SentenceTransformer

class Embedder:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Embed a list of texts into vectors using the loaded model.
        Returns a list of lists of floats.
        """
        return self.model.encode(texts).tolist()