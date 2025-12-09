import re
from typing import Dict


METAPHOR_MAP: Dict[str, str] = {
    "life": "journey",
    "love": "light",
    "darkness": "adversity",
}


def process_metaphors(text: str) -> str:
    """Replace known metaphors in text with abstract concepts."""
    processed = text.lower()
    for metaphor, abstract in METAPHOR_MAP.items():
        processed = re.sub(rf"\b{re.escape(metaphor)}\b", abstract, processed, flags=re.IGNORECASE)
    return processed
