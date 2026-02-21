# apps/retrieval/reranker.py

from typing import List, Dict
from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    """
    Re-ranks retrieved chunks using cross-encoder scoring.
    """

    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query: str, chunks: List[Dict], top_k: int) -> List[Dict]:
        if not chunks:
            return []

        pairs = [(query, chunk["chunk_text"]) for chunk in chunks]
        scores = self.model.predict(pairs)

        for chunk, score in zip(chunks, scores):
            chunk["rerank_score"] = float(score)

        # Sort by rerank score descending
        reranked = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)

        return reranked[:top_k]
