from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .styles import TITLE_STYLE, CORE_STYLE, ENRICHED_STYLE

class Level2Renderer:
    """
    Generates Level 2 PDF: Enhanced Notes Mode
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.doc = SimpleDocTemplate(self.filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        self.elements = []

    def add_slide(self, slide_data: dict, generation_mode: str = "strict"):
        # Slide image
        img_path = slide_data.get("slide_image_path")
        if img_path:
            self.elements.append(Image(img_path, width=4.5*inch, height=3*inch))
            self.elements.append(Spacer(1, 12))

        # Slide title
        title = slide_data.get("slide_title") or f"Slide {slide_data.get('slide_number')}"
        self.elements.append(Paragraph(title, TITLE_STYLE))

        # Core explanation
        core_text = slide_data.get("generated_text", "")
        self.elements.append(Paragraph(core_text, CORE_STYLE))

        # Additional clarification (if enriched mode)
        if generation_mode.lower() == "enriched" and slide_data.get("generated_text"):
            self.elements.append(Paragraph(slide_data.get("generated_text"), ENRICHED_STYLE))

        # Page break after each slide
        self.elements.append(PageBreak())

    def build_pdf(self):
        self.doc.build(self.elements)
