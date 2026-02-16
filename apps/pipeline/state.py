from enum import Enum

class PipelineState(Enum):
    """
    Represents different states in the RAG pipeline.
    LangGraph will use this to track execution progress.
    """
    PENDING = "pending"
    INGESTION_COMPLETED = "ingestion_completed"
    CHUNKING_COMPLETED = "chunking_completed"
    EMBEDDING_COMPLETED = "embedding_completed"
    RETRIEVAL_COMPLETED = "retrieval_completed"
    GENERATION_COMPLETED = "generation_completed"
    PDF_COMPLETED = "pdf_completed"
    FAILED = "failed"
