from typing import List

from . import chains

def get_summary() -> str:
    return chains.get_summary()

def ask(question: str, history: List[tuple[str, str]] | None = None) -> str:
    return chains.ask(question, history)
