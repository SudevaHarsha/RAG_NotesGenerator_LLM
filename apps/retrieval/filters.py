from typing import Dict, Optional

class MetadataFilter:
    """
    Builds metadata filter dictionaries for retrieval.
    """

    @staticmethod
    def build(subject: Optional[str] = None,
              topic: Optional[str] = None,
              academic_level: Optional[str] = None,
              content_type: Optional[str] = None) -> Dict[str, str]:
        filters = {}
        if subject:
            filters["subject"] = subject
        if topic:
            filters["topic"] = topic
        if academic_level:
            filters["academic_level"] = academic_level
        if content_type:
            filters["content_type"] = content_type
        return filters
