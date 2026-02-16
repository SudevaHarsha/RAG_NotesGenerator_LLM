from typing import List, Dict
import numpy as np

from .bge_model import BGEModelLoader


class Embedder:
    """
    Handles embedding of text chunks using BGE model.
    """

    @staticmethod
    def embed_text(text: str) -> List[float]:
        model = BGEModelLoader.get_model()
        embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return embedding.tolist()

    @staticmethod
    def embed_chunks(chunks: List[Dict]) -> List[Dict]:
        """
        Input: List of chunk dictionaries containing 'chunk_text'
        Output: Same list with 'embedding' key added
        """
        print(f"Embedding {len(chunks)} and {chunks[0]} chunks with BGE model...")
        model = BGEModelLoader.get_model()
        texts = [chunk["chunk_text"] for chunk in chunks]
        print(f"Embedding {len(texts)} chunks with BGE model...")

        # Batch encode
        embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        print("Embedding completed.")

        # Assign embeddings back
        for chunk, vector in zip(chunks, embeddings):
            chunk["embedding"] = vector.tolist()
        print("Embeddings assigned to chunks.", chunks[0])

        return chunks
