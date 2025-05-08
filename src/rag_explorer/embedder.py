# src/rag_explorer/embedder.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
embedder.py

Wraps OpenAI embedding model using LangChain to transform
documents into vector representations.
"""

from typing import List
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document


class OpenAIEmbedder:
    """
    Wrapper for the OpenAI Embedding model using LangChain.
    """

    def __init__(self, model: str = "text-embedding-ada-002") -> None:
        """
        Initialize the embedding model.

        Args:
            model: OpenAI embedding model name.
        """
        self.embedder = OpenAIEmbeddings(model=model)

    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """
        Compute embeddings for a list of LangChain Documents.

        Args:
            documents: List of Document objects.

        Returns:
            A list of vector embeddings.
        """
        texts = [doc.page_content for doc in documents]
        return self.embedder.embed_documents(texts)

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query string.

        Args:
            query: The input query text.

        Returns:
            A single vector embedding.
        """
        return self.embedder.embed_query(query)
