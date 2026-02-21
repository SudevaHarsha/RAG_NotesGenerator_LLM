from typing import List, Dict
from collections import defaultdict
from .groq_llm import LangChainGroqLLM
from .prompts import GenerationPrompts
from .slide_assembler import SlideAssembler


class LLMGenerator:
    """
    Generates slide-wise academic notes using slide + transcript enrichment strategy.
    """

    def __init__(self):
        self.llm = LangChainGroqLLM()
        self.prompts = GenerationPrompts()

    def generate_notes(
        self,
        chunks: List[Dict],
        mode: str = "strict"
    ) -> str:
        """
        Generates structured notes slide-by-slide.
        """

        structured_slides = SlideAssembler.assemble(chunks)
        print(f"Structured slides for generation: {structured_slides}")

        final_sections = []

        for slide in structured_slides:

            if mode == "strict":
                print(f"Generating for Slide {slide['slide_number']} in STRICT mode.")
                prompt = GenerationPrompts.STRICT_TEMPLATE.format(
                    slide_text=slide["slide_text"],
                    transcript_text=slide["transcript_text"],
                )

            elif mode == "enriched":
                print(f"Generating for Slide {slide['slide_number']} in ENRICHED mode.")
                prompt = GenerationPrompts.ENRICHED_TEMPLATE.format(
                    slide_text=slide["slide_text"],
                    transcript_text=slide["transcript_text"],
                )

            else:
                raise ValueError("Invalid generation_mode")

            response = self.llm.generate_text(prompt)
            print(f"Generated response for Slide {slide['slide_number']}: {response[:200]}...")  # Log response (truncated for readability)

            section = f"\n\n## Slide {slide['slide_number']}\n\n{response}"
            print(f"Final section for Slide {slide['slide_number']}: {section[:200]}...")  # Log final section (truncated for readability)
            final_sections.append(section)
        print(f"All final sections: {final_sections}...")  # Log all final sections (truncated for readability)
        return "\n".join(final_sections)
