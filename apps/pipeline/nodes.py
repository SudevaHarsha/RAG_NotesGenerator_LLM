# apps/pipeline/nodes.py

from celery import chunks
from apps.ingestion.ingester import SlideIngester
from apps.chunking.custom_chunker import AcademicChunker
from apps.embeddings.embedder import Embedder
from apps.retrieval.retriever import AcademicRetriever
from apps.vectorstore.repository import VectorRepository
from apps.generation.generator import LLMGenerator  # updated generator
from apps.pdf_rendering.level2_renderer import Level2Renderer
from apps.pdf_rendering.level3_renderer import Level3Renderer  # added import
from django.conf import settings
import os

# ------------------------
# Pipeline Node Classes
# ------------------------

class IngestionNode:
    def __init__(self, file_path, course_id):
        self.file_path = file_path
        self.course_id = course_id
        self.ingester = SlideIngester()

    def run(self):
        # Returns list of slide dicts with metadata
        slides = self.ingester.extract_slides(self.file_path, self.course_id)
        return slides


class ChunkingNode:
    def __init__(self, slides):
        self.slides = slides
        self.chunker = AcademicChunker()

    def run(self):
        # Returns academic-aware chunks with metadata
        chunks = self.chunker.chunk_slides(self.slides)
        return chunks


class EmbeddingNode:
    def __init__(self, chunks):
        self.chunks = chunks
        self.embedder = Embedder()

    def run(self):
        # Stores embeddings in vector DB and returns chunks
        embedded_chunks = self.embedder.embed_chunks(self.chunks)
        VectorRepository.store_chunks(embedded_chunks)
        print("Chunks stored in vector repository.")
        return embedded_chunks


class RetrievalNode:
    def __init__(self, embedded_chunks):
        self.embedded_chunks = embedded_chunks
        self.retriever = AcademicRetriever()

    def run(self, question):
        # Returns top-K relevant chunks for the question
        print(f"Retrieving relevant chunks for question: {question}")
        context = self.retriever.retrieve(self.embedded_chunks, question)
        return context


class GenerationNode:
    """
    Updated Generation Node using LangChain Groq LLM via LLMGenerator
    """
    def __init__(self, context, generation_mode="strict"):
        self.context = context
        self.generation_mode = generation_mode
        self.generator = LLMGenerator()  # now uses LangChain Groq

    def run(self):
        # Returns generated content text based on mode (strict/enriched)
        generated_text = self.generator.generate_from_context(
            self.context, 
            question=self.context.get("question", ""), 
            mode=self.generation_mode
        )
        return generated_text


class PDFNode:
    def __init__(self, generated_content, slides_data, output_level="level2"):
        self.generated_content = generated_content
        self.slides_data = slides_data
        self.output_level = output_level

    def run(self):
        # Generate PDF based on level2 or level3
        if self.output_level == "level2":
            renderer = Level2Renderer(self.generated_content, self.slides_data)
        else:
            renderer = Level3Renderer(self.generated_content, self.slides_data)

        filename = renderer.render_pdf()
        return filename
