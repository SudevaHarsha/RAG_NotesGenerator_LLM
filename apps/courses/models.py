from django.db import models


class Course(models.Model):
    """
    Optional structured metadata container.
    A file upload can be linked to a Course,
    or metadata can be provided manually.
    """

    name = models.CharField(max_length=255)

    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    academic_level = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.subject} - {self.academic_level})"
