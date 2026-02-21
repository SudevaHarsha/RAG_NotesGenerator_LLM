# apps/retrieval/contextAssembly.py

from typing import List, Dict


class ContextAssembler:

    @staticmethod
    def assemble(chunks: List[Dict]) -> str:

        slide_map = {}

        for chunk in chunks:
            slide_no = chunk.get("slide_number", 0)
            source = chunk.get("source_type")

            if slide_no not in slide_map:
                slide_map[slide_no] = {
                    "slides": [],
                    "transcripts": [],
                }

            if source == "transcript":
                slide_map[slide_no]["transcripts"].append(chunk["chunk_text"])
            else:
                slide_map[slide_no]["slides"].append(chunk["chunk_text"])

        ordered_slides = sorted(slide_map.keys())

        context_parts = []

        for slide_no in ordered_slides:
            section = slide_map[slide_no]

            if section["slides"]:
                context_parts.append(f"\n=== SLIDE {slide_no} ===\n")
                for s in section["slides"]:
                    context_parts.append(s)

            if section["transcripts"]:
                context_parts.append("\n--- Transcript Explanation ---\n")
                for t in section["transcripts"]:
                    context_parts.append(t)

        return "\n".join(context_parts).strip()
