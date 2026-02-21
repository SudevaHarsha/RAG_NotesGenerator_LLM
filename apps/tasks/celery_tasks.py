# apps/tasks/celery_tasks.py

from celery import Celery, chord, group, shared_task
from django.conf import settings

import os

# LangGraph pipeline imports
from apps.lectures.models import Lecture
from apps.lectures.repository import LectureRepository
from apps.pipeline.nodes import (
    IngestionNode,
    ChunkingNode,
    EmbeddingNode,
    RetrievalNode,
    GenerationNode,
    PDFNode
)

# Async Celery tasks for slide processing and PDF generation
# @shared_task(bind=True)
# def process_slides_task(self, file_path, question, generation_mode, output_level,course_id=None):
#     """
#     Main Celery task to process slides and generate PDF asynchronously
#     """
#     try:
#         # 1️⃣ Ingestion
        
#         ingestion_node = IngestionNode(file_path, course_id)
#         slides_data = ingestion_node.run()  # returns list of slide dicts with metadata

#         # 2️⃣ Chunking
#         chunking_node = ChunkingNode(slides_data)
#         chunks = chunking_node.run()  # returns list of academic-aware chunks

#         # 3️⃣ Embeddings
#         embedding_node = EmbeddingNode(chunks)
#         embedded_chunks = embedding_node.run()  # returns chunks with embeddings stored in vector DB

#         # 4️⃣ Retrieval (for context assembly)
#         retrieval_node = RetrievalNode(embedded_chunks)
#         context = retrieval_node.run(question)  # returns context slices relevant to question

#         # 5️⃣ Generation
#         generation_node = GenerationNode(context, generation_mode=generation_mode)
#         generated_content = generation_node.run()  # returns text content for PDF

#         # 6️⃣ PDF Rendering
#         pdf_node = PDFNode(generated_content, slides_data, output_level=output_level)
#         pdf_filename = pdf_node.run()  # returns filename saved under MEDIA_ROOT

#         return {
#             "status": "success",
#             "pdf_filename": pdf_filename,
#             "pdf_url": os.path.join(settings.MEDIA_URL, pdf_filename)
#         }

#     except Exception as e:
#         # Capture error for debugging
#         return {
#             "status": "failed",
#             "error": str(e)
#         }

@shared_task
def ingest_slides_task(file_path, course_id, lecture_id):
    try:
        ingestion_node = IngestionNode(file_path, course_id)
        slides = ingestion_node.run()

        chunking_node = ChunkingNode(slides)
        chunks = chunking_node.run()

        embedding_node = EmbeddingNode(chunks, lecture_id=lecture_id)
        embedding_node.run()

        return {"status": "slides_done"}
    except Exception as e:
        # 🔥 Delete lecture on failure
        Lecture.objects.filter(id=lecture_id).delete()
        raise e

@shared_task
def ingest_transcript_task(transcript_text, course_id, lecture_id):
    from apps.ingestion.services.transcript_ingestor import TranscriptIngestor

    try:
        transcript_ingestor = TranscriptIngestor()
        transcript_ingestor.ingest(
            course_id=course_id,
            transcript_text=transcript_text,
            lecture_id=lecture_id
        )

        return {"status": "transcript_done"}
    except Exception as e:
        # 🔥 Delete lecture on failure
        Lecture.objects.filter(id=lecture_id).delete()
        raise e
@shared_task
def generate_notes_task(results, question, generation_mode, output_level, lecture_id):

    # Both ingestion tasks finished

    retrieval_node = RetrievalNode(lecture_id)
    context = retrieval_node.run(question)

    generation_node = GenerationNode(context, generation_mode=generation_mode)
    generated_content = generation_node.run()

    pdf_node = PDFNode(generated_content, slides_data=results , output_level=output_level)
    pdf_filename = pdf_node.run()

    return {
        "status": "success",
        "pdf_filename": pdf_filename
    }

@shared_task
def process_lecture_task(
    file_path,
    question,
    generation_mode,
    output_level,
    course_id=None,
    namespace="private",
    subject="General",
    topic="Uncategorized",
):

    lecture = LectureRepository.create_lecture(
        namespace=namespace,
        subject=subject,
        topic=topic,
        academic_level=output_level,
    )

    lecture_id = str(lecture.id)
    ingestion_group = group(
        ingest_slides_task.s(file_path, course_id, lecture_id),
        ingest_transcript_task.s(question, course_id, lecture_id)
    )

    workflow = chord(ingestion_group)(
        generate_notes_task.s(
            question=question,
            generation_mode=generation_mode,
            output_level=output_level,
            lecture_id=lecture_id
        )
    )

    return {"status": "processing_started"}
