from celery import shared_task
from apps.ingestion.services.pdf_extractor import PDFExtractor
from apps.ingestion.services.ppt_extractor import PPTExtractor
from apps.ingestion.services.metadata_builder import MetadataBuilder
from apps.embeddings.embedder import Embedder
from apps.vectorstore.repository import VectorRepository
import os

@shared_task
def ingest_pdf_task(pdf_path: str, subject: str, topic: str, academic_level: str):
    output_image_dir = os.path.join("media", "images")
    slides = PDFExtractor.extract(pdf_path, output_image_dir)
    chunks = MetadataBuilder.build_chunks(slides, subject, topic, academic_level)
    chunks = Embedder.embed_chunks(chunks)
    VectorRepository.store_chunks(chunks)
    return {"status": "success", "total_chunks": len(chunks)}

@shared_task
def ingest_ppt_task(ppt_path: str, subject: str, topic: str, academic_level: str):
    output_image_dir = os.path.join("media", "images")
    slides = PPTExtractor.extract(ppt_path, output_image_dir)
    chunks = MetadataBuilder.build_chunks(slides, subject, topic, academic_level)
    chunks = Embedder.embed_chunks(chunks)
    VectorRepository.store_chunks(chunks)
    return {"status": "success", "total_chunks": len(chunks)}
