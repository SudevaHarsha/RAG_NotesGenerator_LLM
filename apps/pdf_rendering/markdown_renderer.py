# pdfgenerator/markdown_renderer.py

import markdown
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


class MarkdownPDFRenderer:
    """
    Direct Markdown → PDF renderer.
    No slide structuring.
    Renders entire markdown as document.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        self.elements = []
        self.styles = getSampleStyleSheet()

    def add_markdown(self, markdown_text: str):
        # Convert markdown → HTML
        html = markdown.markdown(markdown_text)

        # Split by paragraph
        for block in html.split("\n"):
            if block.strip():
                self.elements.append(
                    Paragraph(block, self.styles["Normal"])
                )
                self.elements.append(Spacer(1, 8))

    def build_pdf(self):
        self.doc.build(self.elements)
