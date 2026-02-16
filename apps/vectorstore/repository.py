from typing import List, Dict, Any, Optional
from django.db.models import F
from django.db import connection
from pgvector.django import CosineDistance

from .models import VectorChunk


class VectorRepository:
    """
    Handles vector storage and retrieval using pgvector.
    """

    @staticmethod
    def store_chunks(chunks: List[Dict[str, Any]]) -> None:
        """
        Bulk insert embedded chunks into PostgreSQL.
        """
        print(f"Storing {len(chunks)} chunks into the vectorstore...")
        objects = [
            VectorChunk(
                namespace=chunk.get("namespace", "private"),
                chunk_text=chunk["chunk_text"],
                embedding=chunk["embedding"],
                slide_number=chunk["slide_number"],
                slide_image_path=chunk.get("slide_image_path"),
                subject=chunk["subject"],
                topic=chunk["topic"],
                academic_level=chunk["academic_level"],
                content_type=chunk["content_type"],
                source_type=chunk.get("source_type", "private_user"),
            )
            for chunk in chunks
        ]
        print(f"Prepared {len(objects)} VectorChunk objects for bulk insertion.")
        VectorChunk.objects.bulk_create(objects, batch_size=100)
        print("Bulk insertion completed.")

    @staticmethod
    def similarity_search(
        query_embedding: List[float],
        top_k: int = 5,
        namespace: str = "private",
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[VectorChunk]:
        """
        Perform cosine similarity search with optional metadata filters.
        """

        queryset = VectorChunk.objects.filter(namespace=namespace)

        # Apply metadata filters dynamically
        if filters:
            queryset = queryset.filter(**filters)

        # Cosine distance ordering (lower is better)
        queryset = queryset.annotate(
            distance=CosineDistance("embedding", query_embedding)
        ).order_by("distance")[:top_k]

        return list(queryset)

    @staticmethod
    def delete_namespace(namespace: str) -> None:
        """
        Utility for future shared/private cleanup.
        """
        VectorChunk.objects.filter(namespace=namespace).delete()

    @staticmethod
    def count_chunks(namespace: str = "private") -> int:
        return VectorChunk.objects.filter(namespace=namespace).count()
