# apps/pipeline/nodes.py

from celery import chunks
from apps.ingestion.ingester import SlideIngester
from apps.chunking.custom_chunker import AcademicChunker
from apps.embeddings.embedder import Embedder
from apps.lectures.repository import LectureRepository
from apps.retrieval.retriever import  NotesRetriever
from apps.vectorstore.repository import VectorRepository
from apps.generation.generator import LLMGenerator  # updated generator
from apps.pdf_rendering.level2_renderer import Level2Renderer
from apps.pdf_rendering.level3_renderer import Level3Renderer  # added import
from apps.pdf_rendering.markdown_renderer import MarkdownPDFRenderer
from apps.pdf_rendering.markdown_parser import MarkdownSlideParser
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
    def __init__(self, chunks, lecture_id=None):
        self.chunks = chunks
        self.lecture_id = lecture_id
        self.embedder = Embedder()

    def run(self):
        # Stores embeddings in vector DB and returns chunks
        embedded_chunks = self.embedder.embed_chunks(self.chunks)

        VectorRepository.store_embedded_chunks(
            lecture_id=self.lecture_id,
            namespace=embedded_chunks[0]["namespace"],
            embedded_chunks=embedded_chunks
        )
        print("Chunks stored in vector repository.")
        return self.lecture_id  # return lecture_id for retrieval context


class RetrievalNode:
    def __init__(self, lecture_id):
        self.lecture_id = lecture_id
        self.retriever = NotesRetriever(lecture_id=lecture_id)

    def run(self, question):
        # Returns top-K relevant chunks for the question
        print(f"Retrieving relevant chunks for question: {question}")
        context = self.retriever.retrieve_notes_context()
        print(f"Retrieved {len(context)} context chunks for generation. and {context}")
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
        generated_text = self.generator.generate_notes(
            self.context, 
            mode=self.generation_mode
        )
        print(f"Generated content length: {len(generated_text)} characters.")
        return generated_text

class PDFNode:
    def __init__(
        self,
        generated_content: str,
        slides_data: list = None,
        output_level: str = "level2",
        render_mode: str = "markdown",  # "structured" or "markdown"
        output_path: str = "output.pdf",
    ):
        self.generated_content = generated_content
        self.slides_data = slides_data or []
        self.output_level = output_level
        self.render_mode = render_mode
        self.output_path = output_path

    def run(self):

        # --------------------------------------------------
        # MODE 1: Structured Rendering (Production Path)
        # --------------------------------------------------
        if self.render_mode == "structured":

            # Parse markdown → structured slides
            structured_slides = MarkdownSlideParser.parse(
                self.generated_content
            )

            # Choose renderer
            if self.output_level == "level2":
                renderer = Level2Renderer(self.output_path)
            else:
                renderer = Level3Renderer(self.output_path)

            # Add slides one by one
            for slide in structured_slides:
                # Attach image path from slides_data if available
                matching_slide = next(
                    (
                        s for s in self.slides_data
                        if s.get("slide_number") == slide.get("slide_number")
                    ),
                    None
                )

                if matching_slide:
                    slide["slide_image_path"] = matching_slide.get("slide_image_path")

                renderer.add_slide(slide, generation_mode="enriched")

            renderer.build_pdf()
            return self.output_path

        # --------------------------------------------------
        # MODE 2: Direct Markdown Rendering (MVP Path)
        # --------------------------------------------------
        elif self.render_mode == "markdown":

            renderer = MarkdownPDFRenderer(self.output_path)
            renderer.add_markdown(self.generated_content)
            renderer.build_pdf()

            return self.output_path

        else:
            raise ValueError("Invalid render_mode. Use 'structured' or 'markdown'.")