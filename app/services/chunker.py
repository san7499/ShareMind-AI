from typing import List, Dict

from app.utils.logger import logger


class TextChunker:
    """
    Splits text into overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.

        Returns:
            List[str]
        """

        if not text or not text.strip():
            logger.warning("Empty text received for chunking.")
            return []

        chunks = []

        step = self.chunk_size - self.chunk_overlap

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += step

        logger.info(f"Generated {len(chunks)} chunks.")

        return chunks

    def split_with_metadata(
        self,
        text: str,
        source: str = ""
    ) -> List[Dict]:
        """
        Split text and include metadata.

        Returns:

        [
            {
                "chunk_id":0,
                "text":"...",
                "source":"HR.pdf",
                "start":0,
                "end":500
            }
        ]
        """

        if not text or not text.strip():
            return []

        documents = []

        step = self.chunk_size - self.chunk_overlap

        start = 0

        chunk_id = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:

                documents.append(
                    {
                        "chunk_id": chunk_id,
                        "text": chunk,
                        "source": source,
                        "start": start,
                        "end": min(end, len(text))
                    }
                )

                chunk_id += 1

            start += step

        logger.info(
            f"Created {len(documents)} metadata chunks."
        )

        return documents


# Singleton instance
text_chunker = TextChunker()