import uuid
from django.db import models


class Lecture(models.Model):
    """
    Represents one uploaded lecture (slides + transcript).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    namespace = models.CharField(max_length=100, db_index=True)
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    academic_level = models.CharField(max_length=100)

    title = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["namespace"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.subject} - {self.topic} ({self.academic_level})"
