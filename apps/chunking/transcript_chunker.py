# import re
# from typing import List, Dict
# from langchain.text_splitter import RecursiveCharacterTextSplitter


# class TranscriptChunker:
#     """
#     Hybrid transcript chunker:
#     - Cleans transcript
#     - Splits into semantic chunks
#     - Maintains chunk index
#     """

#     def __init__(
#         self,
#         chunk_size: int = 800,
#         chunk_overlap: int = 150,
#     ):
#         self.splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap,
#             separators=["\n\n", "\n", ".", " ", ""],
#         )

#     def clean_transcript(self, text: str) -> str:
#         """
#         Remove filler words and normalize whitespace.
#         """
#         filler_patterns = [
#             r"\buh\b",
#             r"\bum\b",
#             r"\bokay\b",
#             r"\bright\b",
#             r"\byou know\b",
#         ]

#         for pattern in filler_patterns:
#             text = re.sub(pattern, "", text, flags=re.IGNORECASE)

#         text = re.sub(r"\s+", " ", text).strip()
#         return text

#     def chunk(self, transcript_text: str) -> List[Dict]:
#         """
#         Returns list of transcript chunks with metadata.
#         """
#         cleaned_text = self.clean_transcript(transcript_text)

#         chunks = self.splitter.split_text(cleaned_text)

#         structured_chunks = []
#         for idx, chunk in enumerate(chunks):
#             structured_chunks.append(
#                 {
#                     "content": chunk,
#                     "metadata": {
#                         "source_type": "transcript",
#                         "chunk_index": idx,
#                     },
#                 }
#             )

#         return structured_chunks

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os

class TranscriptChunker:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def chunk(self, transcript_text: str):
        prompt = f"""
        Split the following lecture transcript into semantic chunks.

        Each chunk should:
        - Cover one concept
        - Be 200-400 words
        - Preserve explanation context

        Transcript:
        {transcript_text}

        Return as numbered sections.
        """

        response = self.llm.invoke([HumanMessage(content=prompt)])
        print(f"LLM response for transcript chunking: {response.content}...")  # Log response (truncated for readability)
        raw_chunks = response.content.split("\n\n")

        structured_chunks = []
        for i, chunk in enumerate(raw_chunks):
            structured_chunks.append({
                "chunk_index": i,
                "chunk_text": chunk.strip()
            })

        return structured_chunks
