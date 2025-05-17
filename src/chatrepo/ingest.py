import os
import stat
import shutil
from pathlib import Path
from typing import Iterable

import git
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .config import DATA_DIR, settings

REPO_DIR = DATA_DIR / "tmp_repo"

def _on_rm_error(func, path, exc_info):
    """Clear the readonly bit and re-invoke *func*."""    
    if os.name == "nt":                           # Windows only                      
        os.chmod(path, stat.S_IWRITE)
    func(path)
        
def sync_repo(repo_url: str) -> Path:
    """Clone or pull *repo_url* and return its local path."""
    if REPO_DIR.exists():
            shutil.rmtree(REPO_DIR, onerror=_on_rm_error)
    git.Repo.clone_from(repo_url, REPO_DIR, depth=1)
    return REPO_DIR

def iter_source_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.suffix in {".py", ".md"} or p.name.lower().startswith("readme"):
            yield p

def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1_000, chunk_overlap=100)
    return splitter.split_text(text)

def run_ingest(repo_url: str) -> list[dict]:
    repo_path = sync_repo(repo_url)
    chunks = []
    for file_path in iter_source_files(repo_path):
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for chunk in chunk_text(text):
            chunks.append(
                {
                    "content": chunk,
                    "metadata": {
                        "path": str(file_path.relative_to(repo_path)),
                        "type": file_path.suffix or "md",
                    },
                }
            )
    return chunks

if __name__ == "__main__":  
    print(f"Ingested {len(run_ingest())} chunks from {settings.repo_url}")
