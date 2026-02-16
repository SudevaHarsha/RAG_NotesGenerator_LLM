from typing import List, Dict
import re
# from chunking.slide_chunker import SlideChunker
from .llm_concept_chunker import GroqLLMConceptChunker

class AcademicChunker:
    # """
    # Custom academic-aware chunker for slides.
    # """

    # def __init__(self, min_chunk_size: int = 50, max_chunk_size: int = 500, overlap_ratio: float = 0.1):
    #     """
    #     Args:
    #         min_chunk_size: Minimum number of characters per chunk
    #         max_chunk_size: Maximum number of characters per chunk
    #         overlap_ratio: Fractional overlap between consecutive chunks (0.1 = 10%)
    #     """
    #     self.min_chunk_size = min_chunk_size
    #     self.max_chunk_size = max_chunk_size
    #     self.overlap_ratio = overlap_ratio

    # def chunk_slides(self, slides: List[Dict]) -> List[Dict]:
    #     """
    #     Input: List of slides with keys:
    #         - slide_number
    #         - title
    #         - bullet_text
    #         - speaker_notes
    #         - slide_image_path
    #         - subject, topic, academic_level, content_type
    #     Output: List of academic-aware chunks
    #     """
    #     all_chunks = []

    #     for slide in slides:
    #         print(f"Processing Slide {slide}")
    #         content = f"{slide.get('title','')}\n{slide.get('bullet_text','')}\n{slide.get('speaker_notes','')}".strip()
    #         print(f"Processing Slide {slide.get('slide_number')}: content length={len(content)} and content is {content[:100]}...")
    #         if not content:
    #             continue

    #         # Split large slides into sub-chunks if necessary
    #         sub_chunks = self._split_content(content)

    #         for sub in sub_chunks:
    #             chunk = {
    #                 "chunk_text": sub,
    #                 "slide_number": slide.get("slide_number"),
    #                 "slide_image_path": slide.get("slide_image_path"),
    #                 "subject": slide.get("subject"),
    #                 "topic": slide.get("topic"),
    #                 "academic_level": slide.get("academic_level"),
    #                 "content_type": slide.get("content_type", "theory"),
    #                 "source_type": slide.get("source_type", "private_user"),
    #                 "namespace": slide.get("namespace", "private"),
    #             }
    #             all_chunks.append(chunk)
    #     print(f"Total chunks created: {len(all_chunks)}")
    #     return all_chunks

    # def _split_content(self, text: str) -> List[str]:
    #     """
    #     Split large text while keeping formulas/definitions intact.
    #     Uses paragraph and sentence breaks intelligently.
    #     """
    #     paragraphs = [p.strip() for p in re.split(r'\n+', text) if p.strip()]
    #     chunks = []
    #     current_chunk = ""

    #     for para in paragraphs:
    #         if len(current_chunk) + len(para) + 1 <= self.max_chunk_size:
    #             current_chunk += ("\n" if current_chunk else "") + para
    #         else:
    #             if len(current_chunk) >= self.min_chunk_size:
    #                 chunks.append(current_chunk)
    #                 # Apply overlap
    #                 overlap_len = int(len(current_chunk) * self.overlap_ratio)
    #                 current_chunk = current_chunk[-overlap_len:] + "\n" + para
    #             else:
    #                 # Merge with current to meet min size
    #                 current_chunk += ("\n" if current_chunk else "") + para

    #     if current_chunk:
    #         chunks.append(current_chunk)

    #     return chunks

    MODEL_NAME = "llama3-70b-8192"

    """
    Unified chunking controller.

    Strategy:
    - Small slide → keep full
    - Medium slide → rule-based splitting
    - Large/complex slide → Groq semantic chunking
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME,
        small_threshold: int = 600,
        large_threshold: int = 1200,
    ):

        # self.tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")
        self.small_threshold = small_threshold
        self.large_threshold = large_threshold

        # self.rule_chunker = SlideChunker()
        self.llm_chunker = GroqLLMConceptChunker(model_name=model_name)

    # --------------------------------------------------
    # Public Entry
    # --------------------------------------------------
    def chunk_slides(self, slides: List[Dict]) -> List[Dict]:
        """
        Iterates through all extracted slides and produces conceptual chunks.
        """
        print(f"🚀 Orchestrating academic chunking for {len(slides)} slides.")
        
        all_final_chunks = []

        for slide_data in slides:
            slide_number = slide_data.get("slide_number", "Unknown")
            slide_text = slide_data.get("chunk_text", "").strip()

            # Skip slides with no extractable text
            if not slide_text:
                print(f"⏩ Skipping Slide {slide_number}: No text content.")
                continue

            print(f"🧠 Chunking Slide {slide_number} with Groq LLM...")

            try:
                # token_count = self._count_tokens(slide_text)

                # --------------------------------------------------
                # 1️⃣ Small → Keep Full Slide
                # --------------------------------------------------
                # if token_count <= self.small_threshold:
                #     return [self._build_full_chunk(slide_data, slide_text)]

                # --------------------------------------------------
                # 2️⃣ Medium → Rule-Based Splitting
                # --------------------------------------------------
                # if self.small_threshold < token_count <= self.large_threshold:
                #     return self.rule_chunker.chunk(slide_data)

                # --------------------------------------------------
                # 3️⃣ Large → LLM Semantic Chunking
                # --------------------------------------------------                concept_chunks = self.llm_chunker.chunk(slide_data)
                concept_chunks = self.llm_chunker.chunk(slide_data)
                # Flatten the list of chunks into our master collection
                all_final_chunks.extend(concept_chunks)
                
            except Exception as e:
                print(f"❌ Error during LLM chunking for Slide {slide_number}: {e}")
                # Fallback: Treat the whole slide as one chunk so data isn't lost
                all_final_chunks.append(self._build_full_chunk(slide_data, slide_text))

        print(f"✅ Finished! Created {len(all_final_chunks)} chunks total.")
        return all_final_chunks

        

    # --------------------------------------------------
    # Token Counter
    # --------------------------------------------------
    # def _count_tokens(self, text: str) -> int:
    #     return len(self.tokenizer.encode(text))

    # --------------------------------------------------
    # Build Full Slide Chunk
    # --------------------------------------------------
    def _build_full_chunk(self, slide_data: Dict, text: str) -> Dict:

        return {
            "text": text,
            "slide_number": slide_data.get("slide_number"),
            "slide_image_path": slide_data.get("slide_image_path"),
            "section_title": "Full Slide",
            "concept_index": 0,
            "subject": slide_data.get("subject"),
            "topic": slide_data.get("topic"),
            "academic_level": slide_data.get("academic_level"),
            "content_type": slide_data.get("content_type"),
            "source_type": slide_data.get("source_type"),
            "namespace": slide_data.get("namespace"),
        }