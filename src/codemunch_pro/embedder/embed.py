"""FastEmbed ONNX embeddings for semantic code search."""

from __future__ import annotations

import logging
from typing import Sequence

logger = logging.getLogger(__name__)

MODEL_NAME = 'BAAI/bge-small-en-v1.5'
EMBEDDING_DIM = 384


class Embedder:
    """Lazy-loading FastEmbed wrapper for code symbol embeddings."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        """Lazy-load the embedding model on first use."""
        if self._model is None:
            from fastembed import TextEmbedding
            logger.info('Loading embedding model: %s', self.model_name)
            self._model = TextEmbedding(model_name=self.model_name)
        return self._model

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Embed a batch of texts.

        Args:
            texts: Sequence of strings to embed.

        Returns:
            List of embedding vectors (each is a list of floats).
        """
        if not texts:
            return []
        return [vec.tolist() for vec in self.model.embed(list(texts))]

    def embed_one(self, text: str) -> list[float]:
        """Embed a single text string."""
        results = self.embed([text])
        return results[0] if results else []

    @staticmethod
    def format_symbol_text(
        name: str,
        kind: str,
        signature: str = '',
        docstring: str = '',
        language: str = '',
    ) -> str:
        """Format a symbol's metadata into a text string for embedding.

        Creates a semantic representation that captures what the symbol does,
        not just its name.
        """
        parts = []
        if language:
            parts.append(f'{language}')
        parts.append(f'{kind}: {name}')
        if signature:
            parts.append(signature)
        if docstring:
            # Truncate long docstrings
            doc = docstring[:200]
            parts.append(doc)
        return ' | '.join(parts)
