import fitz  # PyMuPDF
from typing import List, Dict
import os

class PDFExtractor:
    """
    Extracts slides, text, speaker notes, and images from PDF slides.
    """

    @staticmethod
    def extract(pdf_path: str, output_image_dir: str = None) -> List[Dict]:
        """
        Returns a list of slides with:
        - slide_number
        - title (first line)
        - bullet_text
        - speaker_notes (if any, placeholder empty for now)
        - slide_image_path (if output_image_dir provided)
        """
        slides = []
        doc = fitz.open(pdf_path)
        os.makedirs(output_image_dir, exist_ok=True) if output_image_dir else None

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            title = lines[0] if lines else ""
            bullet_text = "\n".join(lines[1:]) if len(lines) > 1 else ""

            # Slide image extraction
            image_path = None
            if output_image_dir:
                image_path = os.path.join(output_image_dir, f"slide_{page_num}.png")
                pix = page.get_pixmap()
                pix.save(image_path)

            slides.append({
                "slide_number": page_num,
                "title": title,
                "bullet_text": bullet_text,
                "speaker_notes": "",  # PDFs rarely have speaker notes
                "slide_image_path": image_path
            })
        doc.close()
        return slides
