# app/services/rag.py
from typing import List, Dict, Any, Optional

from app.services.embeddings import embedding_service
from app.services.vectordb import vector_db
from app.services.llm import llm_service, LLMService
from app.services.citation import citation_service, CitationService
from app.utils.logger import logger


class RAGService:
    """
    Coordinates the full Retrieval-Augmented Generation (RAG) pipeline:
    1. Retrieve relevant context from ChromaDB
    2. Build enterprise prompt
    3. Delegate chat execution to LLMService
    4. Extract citations via CitationService
    5. Return formatted response
    """

    def __init__(
        self,
        vector_db_instance=vector_db,
        llm_service_instance: LLMService = llm_service,
        citation_service_instance: CitationService = citation_service
    ):
        self.vector_db = vector_db_instance
        self.llm_service = llm_service_instance
        self.citation_service = citation_service_instance
        logger.info("RAGService initialized.")

    def retrieve(self, question: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Generates an embedding for the user's question and searches ChromaDB for matching chunks.
        """
        logger.info(f"Retrieving context for query: '{question}'")
        
        # 1. Embed question
        query_vector = embedding_service.embed_text(question)
        if not query_vector:
            logger.warning("Failed to generate query embedding.")
            return []

        # 2. Search ChromaDB
        results = self.vector_db.search(query_embedding=query_vector, top_k=top_k)
        logger.info(f"Retrieved {len(results)} relevant chunks from VectorDB.")
        return results

    def build_prompt(self, question: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Constructs a structured prompt injecting retrieved chunks as context.
        """
        if not context_chunks:
            formatted_context = "\nNo relevant document context found."
        else:
            formatted_context = "\n" + "\n\n---\n\n".join(
                f"[Source: {item.get('metadata', {}).get('source', item.get('metadata', {}).get('file', 'Unknown'))}, "
                f"Page: {item.get('metadata', {}).get('page', 'N/A')}]\n"
                f"{item['chunk']}"
                for item in context_chunks
            )

        prompt = f"""
You are ShareMind AI, an enterprise assistant.

Answer ONLY using the supplied context.

If the answer is not present in the context,
reply:

"I could not find this information in the authorized SharePoint documents."

-------------------------

Context{formatted_context}

-------------------------

Question: {question}

-------------------------

Answer:
"""
        return prompt

    def answer(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Runs the full RAG pipeline and returns the generated answer with sources and metadata.
        """
        if not question or not question.strip():
            logger.warning("Empty question passed to RAGService.answer().")
            return {
                "answer": "Please provide a valid question.",
                "sources": [],
                "chunks_used": 0,
                "model": self.llm_service.model_name
            }

        try:
            # 1. Retrieve context
            retrieved = self.retrieve(question, top_k=top_k)

            # 2. Extract citations
            sources = self.citation_service.build_sources(retrieved)

            # 3. Build prompt
            prompt = self.build_prompt(question, retrieved)

            # 4. Call LLM Service
            messages = [
                {
                    "role": "system",
                    "content": "You are an enterprise knowledge assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            llm_response_text = self.llm_service.chat(messages)

            logger.info("RAG pipeline execution completed successfully.")
            return {
                "answer": llm_response_text,
                "sources": sources,
                "chunks_used": len(retrieved),
                "model": self.llm_service.model_name
            }

        except Exception:
            logger.exception("RAG Pipeline Failed")
            return {
                "answer": "An error occurred while processing your request in the RAG pipeline.",
                "sources": [],
                "chunks_used": 0,
                "model": self.llm_service.model_name
            }


# Singleton instance for application-wide imports
rag_service = RAGService()