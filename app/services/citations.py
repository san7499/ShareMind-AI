# app/services/citation.py
from typing import List, Dict, Any, Optional
from app.utils.logger import logger


class CitationService:
    """
    Transforms raw retrieved vector database chunks into clean, 
    deduplicated source citations for RAG responses.
    """

    def format_source(self, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extracts and formats relevant citation fields from a chunk's metadata dictionary.
        """
        if not metadata:
            return None

        # Extract file name with common key fallbacks
        file_name = metadata.get("file") or metadata.get("source") or metadata.get("document_name")
        if not file_name:
            file_name = "Unknown Document"

        citation: Dict[str, Any] = {"file": str(file_name)}

        # Add page number if present
        page_num = metadata.get("page") or metadata.get("page_number")
        if page_num is not None:
            citation["page"] = page_num

        # Add optional URL if present
        url = metadata.get("url") or metadata.get("link")
        if url:
            citation["url"] = str(url)

        return citation

    def remove_duplicates(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicates source citations based on file, page, and url properties while preserving order.
        """
        unique_sources: List[Dict[str, Any]] = []
        seen_keys = set()

        for source in sources:
            # Create a unique key tuple based on available fields
            key = (
                source.get("file"),
                source.get("page"),
                source.get("url")
            )

            if key not in seen_keys:
                seen_keys.add(key)
                unique_sources.append(source)

        return unique_sources

    def build_sources(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Converts a list of retrieved chunk dictionaries from VectorDB into unique citations.
        """
        if not results:
            return []

        formatted_sources: List[Dict[str, Any]] = []

        for item in results:
            metadata = item.get("metadata", {})
            source = self.format_source(metadata)
            if source:
                formatted_sources.append(source)

        deduplicated = self.remove_duplicates(formatted_sources)
        logger.info(f"Built {len(deduplicated)} unique citations from {len(results)} chunks.")
        return deduplicated


# Singleton instance for application-wide imports
citation_service = CitationService()