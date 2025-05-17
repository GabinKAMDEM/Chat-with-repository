from typing import List

from . import chains
from .index import build_index as _build_index

def get_summary() -> str:
    return chains.get_summary()

def ask(question: str, history: List[tuple[str, str]] | None = None) -> str:
    return chains.ask(question, history)

def build_index(repo_url: str) -> None:
    """Public wrapper used by Streamlit."""
    _build_index(repo_url)