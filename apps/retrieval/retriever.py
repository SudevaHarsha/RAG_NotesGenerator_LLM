from typing import List, Dict, Optional
from apps.vectorstore.repository import VectorRepository

class AcademicRetriever:
    """
    Handles retrieval of relevant chunks from vectorstore
    """

    def __init__(self, top_k: int = 5, namespace: str = "private"):
        self.top_k = top_k
        self.namespace = namespace

    def retrieve(self, query_embedding: List[float], filters: Optional[Dict[str, str]] = None) -> List[Dict]:
        """
        Retrieves top-K chunks using cosine similarity.
        """
        vector_chunks = VectorRepository.similarity_search(
            query_embedding=query_embedding,
            top_k=self.top_k,
            namespace=self.namespace,
            filters=filters
        )

        results = []
        for vc in vector_chunks:
            results.append({
                "chunk_text": vc.chunk_text,
                "slide_number": vc.slide_number,
                "slide_image_path": vc.slide_image_path,
                "subject": vc.subject,
                "topic": vc.topic,
                "academic_level": vc.academic_level,
                "content_type": vc.content_type,
                "source_type": vc.source_type
            })
        return results
