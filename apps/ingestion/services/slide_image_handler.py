import fitz  # PyMuPDF
from pptx import Presentation
import os
from django.conf import settings

class SlideImageExtractor:
    """
    Extract images for slides from PDF or PPTX
    """
    def __init__(self):
        # This is the line that's likely missing or misspelled!
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'slide_images')
        
        # Also good practice to ensure the folder exists
        os.makedirs(self.output_dir, exist_ok=True)
        
    @staticmethod
    def pdf_to_images(pdf_path: str, output_dir: str):
        import fitz
        os.makedirs(output_dir, exist_ok=True)
        doc = fitz.open(pdf_path)
        for idx, page in enumerate(doc, start=1):
            pix = page.get_pixmap()
            pix.save(os.path.join(output_dir, f"slide_{idx}.png"))
        doc.close()

    @staticmethod
    def ppt_to_images(ppt_path: str, output_dir: str):
        """
        Placeholder: For future image extraction from PPT
        """
        os.makedirs(output_dir, exist_ok=True)
        # Implementation can be done via converting PPT -> PDF -> images
        pass

    def extract(self, slide):
        """
        Unified method expected by SlideIngester.
        slide: dict containing slide info
        Returns: path to extracted image
        """
        print(f"Extracting image for slide: {slide.get('slide_number')}")
        return self.extract_image_from_slide(slide)

    def extract_image_from_slide(self, slide):
        # Your image extraction logic
        slide_number = slide.get("slide_number")
        
        image_path = os.path.join(self.output_dir, f"slide_{slide_number}.png")
        # example: extract image from slide PDF or PPT slide
        # save to image_path
        print(f"Extracted image saved to: {image_path}")
        return str(image_path)