from django.db import models
from pgvector.django import VectorField
from django.contrib.postgres.indexes import GinIndex


class VectorChunk(models.Model):
    """
    Stores embedded academic slide chunks with metadata.
    Designed for pgvector cosine similarity search.
    """

    # Namespace separation (Phase 1: private only, Phase 2+: shared support)
    namespace = models.CharField(max_length=100, default="private")

    # Core content
    chunk_text = models.TextField()

    # Embedding vector (dimension set dynamically by embedding model)
    embedding = VectorField()

    # Slide linkage
    slide_number = models.IntegerField()
    slide_image_path = models.CharField(max_length=500, null=True, blank=True)

    # Academic metadata
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    academic_level = models.CharField(max_length=100)
    content_type = models.CharField(max_length=100)  # theory/example/definition
    source_type = models.CharField(max_length=100, default="private_user")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            GinIndex(
                fields=['chunk_text'],
                name='chunk_text_trgm',
                opclasses=['gin_trgm_ops'],
            ),
        ]

    def __str__(self):
        return f"{self.subject} | Slide {self.slide_number}"
