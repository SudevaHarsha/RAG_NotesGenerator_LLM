from typing import List, Dict
import numpy as np

class Deduplicator:
    """
    Deduplicate retrieved chunks to avoid repetition.
    """

    def __init__(self, similarity_threshold: float = 0.9):
        self.similarity_threshold = similarity_threshold

    def deduplicate(self, chunks: List[Dict], embeddings: List[np.ndarray]) -> List[Dict]:
        """
        Remove duplicates based on cosine similarity between embeddings.
        """
        if not chunks or not embeddings:
            return chunks

        unique_chunks = []
        unique_embeddings = []

        for i, emb in enumerate(embeddings):
            keep = True
            for u_emb in unique_embeddings:
                cosine_sim = np.dot(emb, u_emb) / (np.linalg.norm(emb) * np.linalg.norm(u_emb))
                if cosine_sim >= self.similarity_threshold:
                    keep = False
                    break
            if keep:
                unique_chunks.append(chunks[i])
                unique_embeddings.append(emb)

        return unique_chunks
