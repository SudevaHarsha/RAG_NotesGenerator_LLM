import os
from sentence_transformers import SentenceTransformer
from django.conf import settings

class BGEModelLoader:
    """
    Singleton loader for BAAI BGE embedding model.
    """

    _model_instance = None

    @classmethod
    def get_model(cls):
        if cls._model_instance is None:
            model_name = getattr(settings, "BGE_MODEL_NAME", "BAAI/bge-large-en")
            cls._model_instance = SentenceTransformer(model_name)
        return cls._model_instance
