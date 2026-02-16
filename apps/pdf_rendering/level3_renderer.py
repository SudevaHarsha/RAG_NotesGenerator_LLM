from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .styles import TITLE_STYLE, SECTION_HEADING, CORE_STYLE, ENRICHED_STYLE, DEEP_STYLE

class Level3Renderer:
    """
    Generates Level 3 PDF: Full Teaching Pack Mode
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.doc = SimpleDocTemplate(self.filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        self.elements = []

    def add_table_of_contents(self):
        toc = TableOfContents()
        toc.levelStyles = [
            SECTION_HEADING,
        ]
        self.elements.append(toc)
        self.elements.append(PageBreak())

    def add_slide(self, slide_data: dict, generation_mode: str = "strict"):
        # Slide image
        img_path = slide_data.get("slide_image_path")
        if img_path:
            self.elements.append(Image(img_path, width=4.5*inch, height=3*inch))
            self.elements.append(Spacer(1, 12))

        # Slide title
        title = slide_data.get("slide_title") or f"Slide {slide_data.get('slide_number')}"
        self.elements.append(Paragraph(title, TITLE_STYLE))

        # Section: Concept Overview
        self.elements.append(Paragraph("Concept Overview", SECTION_HEADING))
        self.elements.append(Paragraph(slide_data.get("generated_text", ""), CORE_STYLE))

        # Section: Deep Explanation
        self.elements.append(Paragraph("Deep Explanation", SECTION_HEADING))
        self.elements.append(Paragraph(slide_data.get("generated_text", ""), DEEP_STYLE))

        # Section: Teaching Insights
        self.elements.append(Paragraph("Teaching Insights", SECTION_HEADING))
        self.elements.append(Paragraph(slide_data.get("generated_text", ""), ENRICHED_STYLE))

        # Page break
        self.elements.append(PageBreak())

    def build_pdf(self):
        self.doc.build(self.elements)
