# src/rag_explorer/splitter.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
splitter.py

Split Python code documents into per-function chunks using AST,
and leave other docs intact.
"""

import ast
from typing import List

from langchain.schema import Document


def split_code_by_function(doc: Document) -> List[Document]:
    """
    Split a Python code document into one Document per function.

    Args:
        doc: Document whose page_content is Python source code,
             and metadata must include "source" (file path).

    Returns:
        A list of Documents, each containing a single function’s code
        and metadata["function_name"] set to that function’s name.
        If parsing fails or no functions found, returns [doc].
    """
    code = doc.page_content
    source_path = doc.metadata.get("source", "")
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Return original document cannot be parsed:{e}")
        return [doc]

    lines = code.splitlines()
    split_docs: List[Document] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1
            # Use end_lineno if available (Python 3.8+), else last body line
            end = getattr(node, "end_lineno", node.body[-1].lineno)
            func_lines = lines[start:end]
            func_code = "\n".join(func_lines)
            metadata = doc.metadata.copy()
            metadata["function_name"] = node.name
            split_docs.append(Document(page_content=func_code, metadata=metadata))

    # If no functions found, keep the original doc
    return split_docs or [doc]


def split_documents_by_function(docs: List[Document]) -> List[Document]:
    """
    Apply split_code_by_function to all Python docs, leave others as-is.

    Args:
        docs: List of Document objects.

    Returns:
        Expanded list of Document objects, split per Python function.
    """
    result: List[Document] = []
    for doc in docs:
        source = doc.metadata.get("source", "")
        if source.endswith(".py"):
            result.extend(split_code_by_function(doc))
        else:
            result.append(doc)
    return result
