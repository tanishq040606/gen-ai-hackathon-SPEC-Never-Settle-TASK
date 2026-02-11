from sentence_transformers import SentenceTransformer
import numpy as np

class VectorService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents = []
        self.embeddings = None

    def store(self, text: str):
        # Split text into chunks
        chunks = self.chunk_text(text)

        self.documents = chunks
        self.embeddings = self.model.encode(chunks)

    def semantic_search(self, query: str, k: int = 5):
        if self.embeddings is None or len(self.documents) == 0:
            return []

        query_embedding = self.model.encode([query])[0]

        similarities = np.dot(self.embeddings, query_embedding)

        top_k_indices = similarities.argsort()[-k:][::-1]

        return [self.documents[i] for i in top_k_indices]

    def chunk_text(self, text, chunk_size=500):
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append(chunk)

        return chunks
