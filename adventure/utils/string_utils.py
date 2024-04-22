import re


def strip_numbered_prefixes(text: str) -> str:
    """Strip numbered prefixes from a string.

    Examples: '1. Hello' -> 'Hello', '2) World' -> 'World', 'a) Python' -> 'Python', 'A. Ruby' -> 'Ruby'
    """
    return re.sub(r"^[a-zA-Z]\)|^[0-9]+\.", "", text)
