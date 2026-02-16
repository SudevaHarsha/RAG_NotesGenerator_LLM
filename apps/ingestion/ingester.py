# apps/ingestion/ingester.py

from .services.pdf_extractor import PDFExtractor
from .services.ppt_extractor import PPTExtractor
from .services.slide_image_handler import SlideImageExtractor
from .services.metadata_builder import MetadataBuilder
from apps.courses.models import Course

class SlideIngester:
    """
    Wrapper class to orchestrate slide ingestion for PDF and PPTX
    """
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.ppt_extractor = PPTExtractor()
        self.image_extractor = SlideImageExtractor()
        self.metadata_builder = MetadataBuilder()

    def extract_slides(
        self,
        file_path,
        course_id=None,
    ):
        """
        Extract slides with text, notes, images, and metadata
        """
        print(f"Extracting slides from: {file_path}")
        if file_path.endswith(".pdf"):
            print("Detected PDF file. Using PDFExtractor.")
            slides = self.pdf_extractor.extract(file_path)
        elif file_path.endswith(".pptx"):
            print("Detected PPTX file. Using PPTExtractor.")
            slides = self.ppt_extractor.extract(file_path)
        else:
            raise ValueError("Unsupported file type. Only PDF and PPTX allowed.")

        # Extract images for each slide
        print(f"Extracting images for {len(slides)} slides.")
        for slide in slides:
            slide['image_path'] = self.image_extractor.extract(slide)
            print(f"Slide {slide.get('slide_number')} - Image extracted at: {slide['image_path']}")

        # Build metadata
        subject = "General"
        topic = "Uncategorized"
        academic_level = "Unknown"
        
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                subject = course.subject
                topic = course.topic
                academic_level = course.academic_level
            except Course.DoesNotExist:
                raise Exception("Invalid course_id")

        slides_with_metadata = self.metadata_builder.build_chunks(
            slides,
            subject,
            topic,
            academic_level
        )        
        print(f"Metadata built for {len(slides_with_metadata)} slides.")

        return slides_with_metadata
