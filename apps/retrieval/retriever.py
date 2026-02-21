# apps/retrieval/notes_retriever.py

from typing import List, Dict
from apps.vectorstore.repository import VectorRepository
from apps.retrieval.deduplicator import Deduplicator


class NotesRetriever:
    """
    Query-free retriever for lecture note generation.
    Slides act as structural anchors.
    """

    def __init__(self, namespace: str = "private", transcript_k: int = 3, lecture_id=None):
        self.namespace = namespace
        self.transcript_k = transcript_k
        self.deduplicator = Deduplicator()
        self.lecture_id = lecture_id  # to be set when retrieving context for a specific lecture

    def retrieve_notes_context(
        self,
    ) -> List[Dict]:

        # 1️⃣ Get ALL slide chunks ordered
        slide_chunks = VectorRepository.get_slide_chunks(
            namespace=self.namespace,
            lecture_id=self.lecture_id,
        )
        print(f"Retrieved {len(slide_chunks)} slide chunks for lecture_id {self.lecture_id}. slide chunks: {slide_chunks}")

        # Better approach: directly filter without similarity
        # But keeping consistent with your repository design

        results = []

        for slide in slide_chunks:

            slide_dict = {
                "chunk_text": slide.chunk_text,
                "slide_number": slide.slide_number,
                "source_type": "slide",
                "embedding": slide.embedding,
            }

            results.append(slide_dict)

            # 2️⃣ Retrieve transcript neighbors using slide embedding
            transcript_neighbors = VectorRepository.similarity_search(
                query_embedding=slide.embedding,
                top_k=self.transcript_k,
                namespace=self.namespace,
                lecture_id=self.lecture_id,
                source_type="transcript",
            )
            print(f"Found {len(transcript_neighbors)} transcript neighbors for slide {slide.slide_number}.")

            transcript_dicts = [
                {
                    "chunk_text": t.chunk_text,
                    "slide_number": slide.slide_number,
                    "source_type": "transcript",
                    "embedding": t.embedding,
                }
                for t in transcript_neighbors
            ]
            print(f"Transcript dicts for slide {slide.slide_number}: {transcript_dicts}")

            # 3️⃣ Deduplicate transcripts per slide
            transcript_dicts = self.deduplicator.deduplicate(transcript_dicts)

            print(f"After deduplication, {len(transcript_dicts)} transcript chunks remain for slide {slide.slide_number}.")
            results.extend(transcript_dicts)

        return results
