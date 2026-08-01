from typing import List

from sentence_transformers import SentenceTransformer

from app.utils.logger import logger


class EmbeddingService:
    """
    Generate embeddings using Sentence Transformers.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        logger.info(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        logger.info("Embedding model loaded successfully.")

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text chunk.
        """

        if not text or not text.strip():
            logger.warning("Empty text received.")
            return []

        try:
            vector = self.model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            return vector.tolist()

        except Exception as error:

            logger.error(f"Embedding Error: {error}")

            return []

    def embed_batch(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple chunks.
        """

        if not texts:
            logger.warning("No text chunks received.")
            return []

        try:

            cleaned = [
                text.strip()
                for text in texts
                if text and text.strip()
            ]

            if not cleaned:
                return []

            vectors = self.model.encode(
                cleaned,
                batch_size=32,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            logger.info(
                f"Generated embeddings for {len(cleaned)} chunks."
            )

            return vectors.tolist()

        except Exception as error:

            logger.error(f"Batch Embedding Error: {error}")

            return []


embedding_service = EmbeddingService()