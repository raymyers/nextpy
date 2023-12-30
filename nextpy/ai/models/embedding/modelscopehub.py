# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Wrapper around ModelScopeHub embedding models."""
from typing import Any, List

from pydantic import BaseModel, Extra

from nextpy.ai.models.embedding.base import Embeddings


class ModelScopeEmbeddings(BaseModel, Embeddings):
    """Wrapper around modelscope_hub embedding models.

    To use, you should have the ``modelscope`` python package installed.

    Example:
        .. code-block:: python

            from nextpy.ai.models.embeddings import ModelScopeEmbeddings
            model_id = "damo/nlp_corom_sentence-embedding_english-base"
            embed = ModelScopeEmbeddings(model_id=model_id)
    """

    embed: Any
    model_id: str = "damo/nlp_corom_sentence-embedding_english-base"
    """Model name to use."""

    def __init__(self, **kwargs: Any):
        """Initialize the modelscope."""
        super().__init__(**kwargs)
        try:
            from modelscope.pipelines import pipeline
            from modelscope.utils.constant import Tasks

            self.embed = pipeline(Tasks.sentence_embedding, model=self.model_id)

        except ImportError as e:
            raise ImportError(
                "Could not import some python packages."
                "Please install it with `pip install modelscope`."
            ) from e

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Compute doc embeddings using a modelscope embedding model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        inputs = {"source_sentence": texts}
        embeddings = self.embed(input=inputs)["text_embedding"]
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Compute query embeddings using a modelscope embedding model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        text = text.replace("\n", " ")
        inputs = {"source_sentence": [text]}
        embedding = self.embed(input=inputs)["text_embedding"][0]
        return embedding.tolist()
