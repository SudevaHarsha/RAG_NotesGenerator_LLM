from typing import List, Dict

class ContextAssembler:
    """
    Assembles retrieved chunks into coherent context for LLM.
    """

    @staticmethod
    def assemble(chunks: List[Dict], order_by_slide: bool = True) -> str:
        """
        Concatenate chunks in logical order (slide number) and return text context.
        """
        if order_by_slide:
            chunks = sorted(chunks, key=lambda x: x.get("slide_number", 0))

        context_parts = []
        for chunk in chunks:
            context_parts.append(f"Slide {chunk.get('slide_number')}:\n{chunk.get('chunk_text')}\n")

        return "\n".join(context_parts).strip()
