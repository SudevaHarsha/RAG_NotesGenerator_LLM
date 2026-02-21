from django.db import models
from pgvector.django import VectorField
from apps.lectures.models import Lecture


class VectorChunk(models.Model):
    """
    Stores slide and transcript chunks with embeddings.
    """

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="chunks",
        db_index=True,
    )

    namespace = models.CharField(max_length=100, db_index=True)

    chunk_text = models.TextField()

    embedding = VectorField()

    slide_number = models.IntegerField(null=True, blank=True)

    source_type = models.CharField(
        max_length=50,
        choices=[
            ("private_user", "Slide"),
            ("transcript", "Transcript"),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["lecture", "source_type"]),
            models.Index(fields=["slide_number"]),
        ]
