# src/rag_explorer/loader.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
loader.py

Load project files with specific extensions into Document objects,
preserving each file’s path in metadata.
"""

from pathlib import Path
from langchain.schema import Document
from typing import List
import os

def load_project_documents(project_path: str) -> List[Document]:
    """
    Load project files with specific extensions into Document objects.

    Args:
        project_path: Path to the cloned Git repository.

    Returns:
        A list of Document objects with metadata preserving file paths.
        Returns an empty list in case of errors.
    """
    root = Path(project_path)
    if not root.is_dir():
        raise FileNotFoundError(f"{project_path} is not a valid directory.")

    patterns = [
        "*.py", "*.md", "*.json", "*.yaml",
        "*.yml", "*.sh", "requirements.txt",
    ]
    try:
        docs: List[Document] = []
        for pat in patterns:
            for file in root.rglob(pat):
                text = file.read_text(encoding="utf-8")  # keeps indentation
                docs.append(Document(page_content=text,
                                    metadata={"source": str(file)}))
                return docs
    except Exception as error:
        print(f"Error loading documents from '{project_path}': {error}")
        return []
