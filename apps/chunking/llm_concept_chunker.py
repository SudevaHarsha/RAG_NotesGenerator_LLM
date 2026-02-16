# chunking/llm_concept_chunker.py

from typing import List, Dict
import json
import os

from typer import prompt

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser


MODEL_NAME = "llama3-70b-8192"  # You can change model if needed


class GroqLLMConceptChunker:

    def __init__(self, model_name: str = MODEL_NAME, temperature: float = 0.2):

        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=model_name,
            temperature=temperature
        )

        self.parser = StrOutputParser()

    # --------------------------------------------------
    # Public Entry Point
    # --------------------------------------------------
    def chunk(self, slide_data: Dict) -> List[Dict]:

        print(f"Chunking {len(slide_data)} slides with GroqLLMConceptChunker...")
        slide_text = slide_data.get("chunk_text", "").strip()
        print(f"Chunking Slide {slide_data.get('slide_number')}: content length={len(slide_text)} and content is {slide_text[:100]}...")
        if not slide_text:
            return []

        prompt = self._build_prompt(slide_text)
        print(f"Generated prompt for LLM chunking: {prompt[:500]}...")  # Log the prompt (truncated for readability)
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            raw_output = response.content

            print(f"Raw LLM output: {raw_output[:500]}...")  # Log raw output (truncated for readability)
            parsed_chunks = self._safe_json_parse(raw_output)

            if not parsed_chunks:
                return [self._build_chunk(slide_data, slide_text, "Full Slide", 0)]

            print(f"Parsed chunks: {parsed_chunks[:2]}...")  # Log parsed chunks (truncated for readability)
            return [
                self._build_chunk(
                    slide_data=slide_data,
                    text=item.get("content", ""),
                    section_title=item.get("title", f"Concept {idx}"),
                    concept_index=idx
                )
                for idx, item in enumerate(parsed_chunks)
            ]

        except Exception as e:
            # Fail-safe fallback
            return [self._build_chunk(slide_data, slide_text, "Full Slide", 0)]

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------
    def _build_prompt(self, slide_text: str) -> str:
        return f"""
You are a semantic chunking engine for a RAG system.

Your task:
Split the slide into meaningful conceptual chunks.

Rules:
- Each chunk must represent ONE complete idea.
- Do NOT split randomly.
- Keep related bullet points together.
- Return ONLY valid JSON.
- Do NOT add explanations.

Output format:
[
  {{
    "title": "Concept title",
    "content": "Full text of that concept"
  }}
]

Slide:
{slide_text}
"""

    # --------------------------------------------------
    # JSON Safe Parsing
    # --------------------------------------------------
    def _safe_json_parse(self, text: str):

        try:
            return json.loads(text)
        except Exception:
            # Try extracting JSON block
            try:
                start = text.index("[")
                end = text.rindex("]") + 1
                return json.loads(text[start:end])
            except Exception:
                return None

    # --------------------------------------------------
    # Build Final Chunk
    # --------------------------------------------------
    def _build_chunk(self,
                     slide_data: Dict,
                     text: str,
                     section_title: str,
                     concept_index: int):

        return {
            "chunk_text": text.strip(),
            "slide_number": slide_data.get("slide_number"),
            "slide_image_path": slide_data.get("slide_image_path"),
            "section_title": section_title,
            "concept_index": concept_index,
            "subject": slide_data.get("subject"),
            "topic": slide_data.get("topic"),
            "academic_level": slide_data.get("academic_level"),
            "content_type": slide_data.get("content_type"),
            "source_type": slide_data.get("source_type"),
            "namespace": slide_data.get("namespace"),
        }
