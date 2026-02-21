# apps/vectorstore/repository.py
from typing import List, Dict
from apps.lectures.models import Lecture
from apps.vectorstore.models import VectorChunk
from pgvector.django import CosineDistance

class VectorRepository:

    @staticmethod
    @staticmethod
    def store_embedded_chunks(
        lecture_id,
        namespace: str,
        embedded_chunks: List[Dict],
    ):
        """
        Bulk create VectorChunk records after embedding stage.

        embedded_chunks format:
        [
            {
                "text": str,
                "embedding": List[float],
                "slide_number": int | None,
                "source_type": "private_user" | "transcript",
            }
        ]
        """

        lecture = Lecture.objects.get(id=lecture_id)

        objects_to_create = []

        for chunk in embedded_chunks:
            obj = VectorChunk(
                lecture=lecture,
                namespace=namespace,
                chunk_text=chunk["chunk_text"],
                embedding=chunk["embedding"],
                slide_number=chunk.get("slide_number"),
                source_type=chunk["source_type"],
            )
            objects_to_create.append(obj)

        VectorChunk.objects.bulk_create(objects_to_create, batch_size=500)

        return len(objects_to_create)

    @staticmethod
    def get_slide_chunks(namespace: str, lecture_id):
        return VectorChunk.objects.filter(
            namespace=namespace,
            lecture_id=lecture_id,
            source_type="slides",
        ).order_by("slide_number")

    @staticmethod
    def similarity_search(
        query_embedding,
        top_k,
        namespace,
        lecture_id,
        source_type,
    ):
        queryset = VectorChunk.objects.filter(
            namespace=namespace,
            lecture_id=lecture_id,
            source_type=source_type,
        )

        results = VectorChunk.objects.annotate(
        distance=CosineDistance('embedding', query_embedding)
        ).order_by('distance')[:top_k]
        
        return results

    @staticmethod
    def delete_namespace(namespace: str) -> None:
        """
        Utility for future shared/private cleanup.
        """
        VectorChunk.objects.filter(namespace=namespace).delete()
        
    def get_all_slides(filters):
        return VectorChunk.objects.filter(
            source_type="private_user",
            **filters
        ).order_by("slide_number")

    @staticmethod
    def count_chunks(namespace: str = "private") -> int:
        return VectorChunk.objects.filter(namespace=namespace).count()
