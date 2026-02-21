from typing import List, Dict

class MetadataBuilder:
    """
    Converts raw slide extraction into metadata-rich chunk objects
    suitable for embedding and vector storage.
    """

    @staticmethod
    def build_chunks(slides: List[Dict], subject: str, topic: str, academic_level: str) -> List[Dict]:
        chunks = []
        for slide in slides:
            content_text = f"{slide['title']}\n{slide['bullet_text']}\n{slide['speaker_notes']}".strip()
            if not content_text:
                continue

            chunk = {
                "source_type": "slide",
                "chunk_text": content_text,
                "slide_number": slide["slide_number"],
                "slide_image_path": slide.get("image_path"),
                "subject": subject,
                "topic": topic,
                "academic_level": academic_level,
                "content_type": "theory",  # default, can be adjusted
                "source_type": "slides",
                "namespace": "private",
            }
            print(f"Built chunk for Slide {slide['slide_number']}: {chunk}...")  # Log chunk creation (truncated for readability)
            chunks.append(chunk)
        return chunks
