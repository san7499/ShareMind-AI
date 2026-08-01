import os
import uuid
from typing import List, Dict, Any, Optional, Union

try:
    import chromadb
except ImportError:
    chromadb = None

from app.config import CHROMA_DB_PATH
from app.utils.logger import logger


class VectorDB:
    """
    ChromaDB Service

    Responsible for:
    - Creating collections
    - Storing document embeddings
    - Similarity search
    - Collection management
    """

    def __init__(
        self,
        collection_name: str = "rag_documents",
        persist_directory: Optional[str] = CHROMA_DB_PATH,
    ):

        if chromadb is None:
            raise ImportError(
                "ChromaDB is not installed.\n"
                "Run: pip install chromadb"
            )

        self.collection_name = collection_name

        if persist_directory:

            os.makedirs(persist_directory, exist_ok=True)

            logger.info(
                f"Initializing Persistent ChromaDB at {persist_directory}"
            )

            self.client = chromadb.PersistentClient(
                path=persist_directory
            )

        else:

            logger.info(
                "Initializing In-Memory ChromaDB"
            )

            self.client = chromadb.EphemeralClient()

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={
                "hnsw:space": "cosine"
            }
        )

        logger.info(
            f"Collection '{self.collection_name}' ready."
        )

    # --------------------------------------------------------

    def add_documents(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> bool:
        """
        Store document chunks into ChromaDB.
        """

        if not chunks:
            logger.warning("No chunks supplied.")
            return False

        if not embeddings:
            logger.warning("No embeddings supplied.")
            return False

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Chunks and embeddings count mismatch."
            )

        if metadatas is not None:

            if len(metadatas) != len(chunks):
                raise ValueError(
                    "Metadata count mismatch."
                )

        else:

            metadatas = [
                {"chunk_index": i}
                for i in range(len(chunks))
            ]

        if ids is None:

            ids = [
                str(uuid.uuid4())
                for _ in chunks
            ]

        try:

            self.collection.add(
                ids=ids,
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            logger.info(
                f"Stored {len(chunks)} chunks."
            )

            return True

        except Exception as error:

            logger.error(
                f"VectorDB Insert Error: {error}"
            )

            return False

    # --------------------------------------------------------

    def search(
        self,
        query_embedding: Union[
            List[float],
            List[List[float]]
        ],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Semantic similarity search.
        """

        if not query_embedding:
            return []

        if isinstance(query_embedding[0], (float, int)):
            query_embeddings = [query_embedding]
        else:
            query_embeddings = query_embedding

        try:

            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=top_k,
                include=[
                    "documents",
                    "metadatas",
                    "distances",
                ],
            )

            output = []

            if not results.get("documents"):
                return output

            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]

            for doc, meta, distance in zip(
                documents,
                metadatas,
                distances,
            ):

                output.append(
                    {
                        "chunk": doc,
                        "metadata": meta,
                        "distance": distance,
                    }
                )

            logger.info(
                f"Retrieved {len(output)} chunks."
            )

            return output

        except Exception as error:

            logger.error(
                f"Search Error: {error}"
            )

            return []

    # --------------------------------------------------------

    def delete_document(
        self,
        document_id: str,
    ) -> bool:
        """
        Delete one document by ID.
        """

        try:

            self.collection.delete(
                ids=[document_id]
            )

            logger.info(
                f"Deleted {document_id}"
            )

            return True

        except Exception as error:

            logger.error(
                f"Delete Error: {error}"
            )

            return False

    # --------------------------------------------------------

    def count(self) -> int:
        """
        Number of indexed chunks.
        """

        return self.collection.count()

    # --------------------------------------------------------

    def reset_collection(self) -> bool:
        """
        Delete all indexed data.
        """

        try:

            self.client.delete_collection(
                self.collection_name
            )

            self.collection = (
                self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={
                        "hnsw:space": "cosine"
                    },
                )
            )

            logger.info(
                "Collection reset successfully."
            )

            return True

        except Exception as error:

            logger.error(
                f"Reset Error: {error}"
            )

            return False

    # --------------------------------------------------------

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Return collection statistics.
        """

        return {
            "collection_name": self.collection_name,
            "document_count": self.count(),
        }


# Singleton instance
vector_db = VectorDB()