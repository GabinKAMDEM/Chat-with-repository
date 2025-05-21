
from pathlib import Path
import json
from typing import List

from . import chains
from .config import DATA_DIR
from .index import build_index as _build_index

_SYMBOLS_FILE = DATA_DIR / "symbols.json"

def build_index(repo_url: str) -> None:
    """Clone, parse and embed *repo_url* into the vector store."""
    _build_index(repo_url)

def get_summary(thread_id : str | None = None) -> str:
    """Return an executive summary of the current repository."""
    return chains.get_summary(thread_id=thread_id)

def ask(question: str, thread_id : str | None = None , history: List[tuple[str, str]] | None = None) -> str:
    """Answer *question* while taking *history* into account."""
    return chains.ask(question, thread_id=thread_id)

def reset_chat() -> None:
    """Clear the conversational memory/state in the chains module."""
    chains.reset_chat()

def _load_symbols() -> list[dict]:
    if not _SYMBOLS_FILE.exists():
        return []
    return json.loads(_SYMBOLS_FILE.read_text())

def list_modules() -> list[str]:
    """Return a sorted list of top‑level modules/packages in the repo."""
    symbols = _load_symbols()
    return sorted({Path(s["path"]).parts[0] for s in symbols})

def list_symbols(module: str) -> list[dict]:
    """Return all symbols (functions/classes) belonging to *module*."""
    return [s for s in _load_symbols() if s["path"].startswith(module)]
