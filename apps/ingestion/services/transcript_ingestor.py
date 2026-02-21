# apps/ingestion/services/transcript_ingestor.py

from apps.chunking.transcript_chunker import TranscriptChunker
from apps.embeddings.transcript_embedder import TranscriptEmbedder


class TranscriptIngestor:

    def __init__(self):
        self.chunker = TranscriptChunker()
        self.embedder = TranscriptEmbedder()

    def ingest(
        self,
        transcript_text: str,
        namespace: str = "private",
        course_id = None,
        lecture_id = None
    ):
        # 1️⃣ Chunk transcript
        chunks = self.chunker.chunk(transcript_text)
        print(f"Transcript chunked into {len(chunks)} chunks.")

        subject = "General"
        topic = "Uncategorized"
        academic_level = "Unknown"
        
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                subject = course.subject
                topic = course.topic
                academic_level = course.academic_level
            except Course.DoesNotExist:
                raise Exception("Invalid course_id")
        
        # 2️⃣ Embed + Store using YOUR vector repository
        self.embedder.embed_and_store(
            chunks=chunks,
            subject=subject,
            topic=topic,
            academic_level=academic_level,
            namespace=namespace,
            lecture_id=lecture_id
        )
        print(f"Transcript ingested with {len(chunks)} chunks....................................................")   