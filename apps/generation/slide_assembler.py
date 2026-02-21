from collections import defaultdict


class SlideAssembler:
    """
    Groups retrieved chunks by slide number and
    merges slide + transcript content.
    """

    @staticmethod
    def assemble(context_chunks):

        slides = defaultdict(lambda: {
            "slide_text": "",
            "transcript_text": []
        })

        for chunk in context_chunks:

            slide_number = chunk["slide_number"]

            if chunk["source_type"] == "slide":
                slides[slide_number]["slide_text"] = chunk["chunk_text"]

            elif chunk["source_type"] == "transcript":
                slides[slide_number]["transcript_text"].append(
                    chunk["chunk_text"]
                )

        # Convert to ordered list
        structured_slides = []

        for slide_number in sorted(slides.keys()):
            structured_slides.append({
                "slide_number": slide_number,
                "slide_text": slides[slide_number]["slide_text"],
                "transcript_text": "\n\n".join(
                    slides[slide_number]["transcript_text"]
                )
            })

        return structured_slides
