from typing import List, Dict

from apps.vectorstore.repository import VectorRepository
from apps.embeddings.embedder import Embedder  # your BGE embedder


class TranscriptEmbedder:
    """
    Uses same BGE embedding model as slides.
    """

    @staticmethod
    def embed_and_store(
        chunks: List[Dict],
        subject: str,
        topic: str,
        academic_level: str,
        namespace: str = "private",
        lecture_id = None
    ) -> None:
        """
        Expects chunks in format:
        [
            {"chunk_text": "..."},
            ...
        ]
        """

        # 1️⃣ Add metadata required by VectorChunk
        prepared_chunks = []
        for chunk in chunks:
            prepared_chunks.append({
                "namespace": namespace,
                "chunk_text": chunk["chunk_text"],
                "slide_number": 0,  # transcripts not tied to slides
                "slide_image_path": None,
                "subject": subject,
                "topic": topic,
                "academic_level": academic_level,
                "content_type": "explanation",
                "source_type": "transcript",
            })

        # 2️⃣ Embed using SAME BGE model
        embedded_chunks = Embedder.embed_chunks(prepared_chunks)

        # 3️⃣ Store using your existing repository
        VectorRepository.store_embedded_chunks(
            lecture_id=lecture_id,
            namespace=namespace,
            embedded_chunks=embedded_chunks
        )
