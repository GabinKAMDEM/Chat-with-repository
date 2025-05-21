"""
Ingest repository by cloning, parsing, splitting, and chunking files.
"""
import os
import git
import stat
import shutil
from pathlib import Path
from typing import Iterable
from .parser import parse_repo, save_symbols
from .config import DATA_DIR, settings
from langchain.text_splitter import RecursiveCharacterTextSplitter

REPO_DIR = DATA_DIR / "tmp_repo"
code_splitter = RecursiveCharacterTextSplitter(
    separators=["\nclass ", "\ndef ", "\n@", "\n\n"],
    chunk_size=800,
    chunk_overlap=100,
    keep_separator=True,
)
md_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

def _on_rm_error(func, path, exc_info):
    """Clear the readonly bit and re-invoke *func*."""    
    os.chmod(path, stat.S_IWRITE)
    func(path)
        
def sync_repo(repo_url: str) -> Path:
    """Clone or pull *repo_url* and return its local path."""
    if REPO_DIR.exists():
            shutil.rmtree(REPO_DIR, onerror=_on_rm_error)
    git.Repo.clone_from(repo_url, REPO_DIR, depth=1)
    shutil.rmtree(os.path.join(REPO_DIR, ".git"), onerror=_on_rm_error)
    return REPO_DIR

def iter_source_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.suffix in {".py", ".md"} or p.name.lower().startswith("readme"):
            yield p

def chunk_text(path: Path, text: str) -> list[str]:
    splitter = code_splitter if path.suffix == ".py" else md_splitter
    return splitter.split_text(text)

def run_ingest(repo_url: str) -> list[dict]:
    """Ingest repository: parse symbols, save them, and chunk all files."""
    repo_path = sync_repo(repo_url)
    symbols = parse_repo(repo_path)
    save_symbols(symbols, DATA_DIR / "symbols.json")

    chunks = []
    for file_path in iter_source_files(repo_path):
        raw = file_path.read_text(encoding="utf-8", errors="ignore")
        for chunk in chunk_text(file_path, raw):
            chunks.append(
                {
                    "content": chunk,
                    "metadata": {
                        "path": str(file_path.relative_to(repo_path)),
                    },
                }
            )

        # 2) docstrings de symboles (déjà existants)
        for sym in symbols:
            chunks.append(
                {
                    "content": f"# {sym['signature']}\n {sym['docstring']}",
                    "metadata": {**sym, "type": "symbol"},
                }
            )     
    return chunks

if __name__ == "__main__":  
    print(f"✅ Ingested {len(run_ingest())} chunks from {settings.repo_url}")
