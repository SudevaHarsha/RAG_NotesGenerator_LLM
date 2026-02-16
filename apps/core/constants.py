"""
Shared constants for the Academic RAG system.
Used across ingestion, chunking, embeddings, retrieval, generation, and PDF rendering.
"""

# ---------------------------
# General constants
# ---------------------------
MAX_SLIDE_IMAGE_WIDTH = 800        # Max width in pixels for slide images in PDF
PDF_PAGE_MARGIN = 50               # Margin in points
DEFAULT_TOP_K = 5                  # Default Top-K retrieval chunks
CHUNK_OVERLAP_RATIO = 0.1          # 10% overlap when necessary
CHUNK_MIN_LENGTH = 50              # Minimum characters in a chunk
CHUNK_MAX_LENGTH = 1000            # Maximum characters in a chunk

# ---------------------------
# Content Types
# ---------------------------
CONTENT_TYPE_THEORY = "theory"
CONTENT_TYPE_EXAMPLE = "example"
CONTENT_TYPE_DEFINITION = "definition"

# ---------------------------
# Source Types
# ---------------------------
SOURCE_TYPE_PRIVATE = "private_user"
SOURCE_TYPE_SHARED = "shared_corpus"

# ---------------------------
# PDF Levels
# ---------------------------
PDF_LEVEL_2 = "level2"  # Enhanced Notes
PDF_LEVEL_3 = "level3"  # Full Teaching Pack

# ---------------------------
# Generation Modes
# ---------------------------
GENERATION_MODE_STRICT = "strict"
GENERATION_MODE_ENRICHED = "enriched"
