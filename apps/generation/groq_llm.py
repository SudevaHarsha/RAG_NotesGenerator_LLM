from langchain_groq import ChatGroq

class LangChainGroqLLM:
    """
    LangChain Groq LLM wrapper using the official langchain-groq package.
    """

    def __init__(self, model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.0, max_tokens: int = 1024):
        self.llm = ChatGroq(
            model=model_name,
            groq_api_key=None  # LangChain Groq picks up GROQ_API_KEY from env automatically
        )
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate a response using the Groq model via LangChain.
        """
        # Call the model directly
        response = self.llm.invoke(
            [
                {"role": "user", "content": prompt}
            ]
        )
        return response.content
