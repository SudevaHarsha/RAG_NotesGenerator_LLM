import re

class MarkdownSlideParser:
    """
    Converts LLM markdown slide output into structured slide dicts.
    """

    SLIDE_PATTERN = r"##\s*Slide\s*(\d+):?\s*(.*)"

    @staticmethod
    def parse(markdown_text: str):
        slides = []
        current_slide = None

        lines = markdown_text.splitlines()

        for line in lines:
            header_match = re.match(MarkdownSlideParser.SLIDE_PATTERN, line.strip())

            if header_match:
                # Save previous slide
                if current_slide:
                    slides.append(current_slide)

                slide_number = int(header_match.group(1))
                slide_title = header_match.group(2).strip()

                current_slide = {
                    "slide_number": slide_number,
                    "slide_title": slide_title,
                    "sections": {
                        "overview": "",
                        "deep": "",
                        "teaching_insights": ""
                    }
                }
            else:
                if current_slide:
                    current_slide["sections"]["overview"] += line + "\n"

        if current_slide:
            slides.append(current_slide)

        return slides
