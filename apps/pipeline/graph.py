from typing import Dict, Any
from apps.pipeline.state import PipelineState
from apps.pipeline.nodes import (
    IngestionNode,
    ChunkingNode,
    EmbeddingNode,
    RetrievalNode,
    GenerationNode,
    PDFNode
)

class LangGraph:
    """
    Orchestrates the state-driven execution of the RAG pipeline.
    """

    def __init__(self, file_path: str, question: str, generation_mode: str, output_level: str):
        self.file_path = file_path
        self.question = question
        self.generation_mode = generation_mode
        self.output_level = output_level
        self.state = PipelineState.PENDING
        self.context: Dict[str, Any] = {}  # Stores intermediate results

    def run(self) -> Dict[str, Any]:
        try:
            # 1️⃣ Ingestion
            ingestion_node = IngestionNode()
            slides = ingestion_node.run(self.file_path)
            self.context["slides"] = slides
            self.state = PipelineState.INGESTION_COMPLETED

            # 2️⃣ Chunking
            chunking_node = ChunkingNode()
            chunks = chunking_node.run(slides)
            self.context["chunks"] = chunks
            self.state = PipelineState.CHUNKING_COMPLETED

            # 3️⃣ Embedding
            embedding_node = EmbeddingNode()
            embedding_node.run(chunks)
            self.state = PipelineState.EMBEDDING_COMPLETED

            # 4️⃣ Retrieval
            retrieval_node = RetrievalNode()
            retrieved_chunks = retrieval_node.run(self.question)
            self.context["retrieved_chunks"] = retrieved_chunks
            self.state = PipelineState.RETRIEVAL_COMPLETED

            # 5️⃣ Generation
            generation_node = GenerationNode()
            generated_slides = generation_node.run(retrieved_chunks, self.question, self.generation_mode)
            self.context["generated_slides"] = generated_slides
            self.state = PipelineState.GENERATION_COMPLETED

            # 6️⃣ PDF Rendering
            pdf_node = PDFNode()
            pdf_path = pdf_node.run(generated_slides, self.generation_mode, self.output_level)
            self.context["pdf_path"] = pdf_path
            self.state = PipelineState.PDF_COMPLETED

            return {"status": "success", "pdf_path": pdf_path}

        except Exception as e:
            self.state = PipelineState.FAILED
            return {"status": "failed", "error": str(e)}
