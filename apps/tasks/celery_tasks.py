# apps/tasks/celery_tasks.py

from celery import Celery, shared_task
from django.conf import settings

import os

# LangGraph pipeline imports
from apps.pipeline.nodes import (
    IngestionNode,
    ChunkingNode,
    EmbeddingNode,
    RetrievalNode,
    GenerationNode,
    PDFNode
)

# Async Celery tasks for slide processing and PDF generation
@shared_task(bind=True)
def process_slides_task(self, file_path, question, generation_mode, output_level,course_id=None):
    """
    Main Celery task to process slides and generate PDF asynchronously
    """
    try:
        # 1️⃣ Ingestion
        
        ingestion_node = IngestionNode(file_path, course_id)
        slides_data = ingestion_node.run()  # returns list of slide dicts with metadata

        # 2️⃣ Chunking
        chunking_node = ChunkingNode(slides_data)
        chunks = chunking_node.run()  # returns list of academic-aware chunks

        # 3️⃣ Embeddings
        embedding_node = EmbeddingNode(chunks)
        embedded_chunks = embedding_node.run()  # returns chunks with embeddings stored in vector DB

        # 4️⃣ Retrieval (for context assembly)
        retrieval_node = RetrievalNode(embedded_chunks)
        context = retrieval_node.run(question)  # returns context slices relevant to question

        # 5️⃣ Generation
        generation_node = GenerationNode(context, generation_mode=generation_mode)
        generated_content = generation_node.run()  # returns text content for PDF

        # 6️⃣ PDF Rendering
        pdf_node = PDFNode(generated_content, slides_data, output_level=output_level)
        pdf_filename = pdf_node.run()  # returns filename saved under MEDIA_ROOT

        return {
            "status": "success",
            "pdf_filename": pdf_filename,
            "pdf_url": os.path.join(settings.MEDIA_URL, pdf_filename)
        }

    except Exception as e:
        # Capture error for debugging
        return {
            "status": "failed",
            "error": str(e)
        }
