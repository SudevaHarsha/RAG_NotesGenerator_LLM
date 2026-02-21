class GenerationPrompts:

    STRICT_TEMPLATE = """
You are an academic assistant.

Generate structured academic notes ONLY from the content below.
Do not introduce external facts.

Slide Content:
{slide_text}

Transcript Explanation:
{transcript_text}

Produce clear, structured notes.
"""

    ENRICHED_TEMPLATE = """
You are an academic teaching assistant.

Generate detailed academic notes based on:

Slide Content:
{slide_text}

Transcript Explanation:
{transcript_text}

Instructions:
- Expand explanations clearly
- Add a section titled 'Additional Clarification'
- You may include examples or analogies
- Do NOT introduce new core formulas or facts

Produce well-structured notes.
"""
