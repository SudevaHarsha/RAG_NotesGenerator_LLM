from typing import List, Dict
from .groq_llm import LangChainGroqLLM
from .prompts import GenerationPrompts

class LLMGenerator:
    """
    Generates dual-mode output using the langchain-groq LLM.
    """

    def __init__(self):
        self.llm = LangChainGroqLLM()

    def generate_from_context(self, chunks: List[Dict], question: str, mode: str = "strict") -> str:
        """
        Generate an answer given retrieved context using Groq model via LangChain.
        """
        context_text = "\n\n".join([c["chunk_text"] for c in chunks])

        if mode == "strict":
            prompt = GenerationPrompts.STRICT_TEMPLATE.format(context=context_text, question=question)
        elif mode == "enriched":
            prompt = GenerationPrompts.ENRICHED_TEMPLATE.format(context=context_text, question=question)
        else:
            raise ValueError("Invalid generation_mode, choose 'strict' or 'enriched'")

        # Use the LangChain Groq model
        return self.llm.generate_text(prompt)
