from typing import List, Dict
import numpy as np


class Deduplicator:
    """
    Production-grade deduplicator.

    - Uses cosine similarity (optimized for normalized embeddings)
    - Preserves higher rerank_score when duplicates exist
    - Keeps structural diversity across slides
    """

    def __init__(self, similarity_threshold: float = 0.93):
        self.similarity_threshold = similarity_threshold

    def deduplicate(self, chunks: List[Dict]) -> List[Dict]:

        if not chunks:
            return []

        unique_chunks: List[Dict] = []
        unique_embeddings: List[np.ndarray] = []

        for chunk in chunks:
            current_embedding = np.array(chunk["embedding"])

            keep = True
            replace_index = None

            for i, existing_embedding in enumerate(unique_embeddings):

                # Since embeddings are normalized → cosine = dot product
                cosine_sim = np.dot(current_embedding, existing_embedding)

                if cosine_sim >= self.similarity_threshold:
                    keep = False

                    # If rerank_score exists, prefer higher one
                    if (
                        "rerank_score" in chunk
                        and "rerank_score" in unique_chunks[i]
                        and chunk["rerank_score"] > unique_chunks[i]["rerank_score"]
                    ):
                        replace_index = i
                    break

            if keep:
                unique_chunks.append(chunk)
                unique_embeddings.append(current_embedding)

            elif replace_index is not None:
                unique_chunks[replace_index] = chunk
                unique_embeddings[replace_index] = current_embedding

        return unique_chunks
