# app/services/llm.py
from typing import List, Dict, Any, Optional

try:
    import ollama
except ImportError:
    ollama = None

from app.config import OLLAMA_MODEL, OLLAMA_URL
from app.utils.logger import logger


class LLMService:
    """
    Handles interactions with the local Ollama LLM instance.
    """

    def __init__(
        self, 
        model_name: str = OLLAMA_MODEL, 
        base_url: Optional[str] = OLLAMA_URL
    ):
        if ollama is None:
            raise ImportError(
                "The 'ollama' library is not installed. "
                "Please run: pip install ollama"
            )

        self.model_name = model_name
        self.base_url = base_url

        if self.base_url:
            self.client = ollama.Client(host=self.base_url)
        else:
            self.client = ollama.Client()

        logger.info(f"LLMService initialized with model '{self.model_name}'.")

    def generate(self, prompt: str) -> str:
        """
        Return a single text completion for a given prompt.
        """
        if not prompt or not prompt.strip():
            logger.warning("Empty prompt passed to LLMService.generate().")
            return ""

        try:
            logger.info(f"Sending completion request to Ollama ({self.model_name})...")
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt
            )
            text = response.get("response", "").strip()
            
            if not text:
                logger.warning("Ollama returned an empty completion response.")
                return "The language model returned an empty response."

            return text

        except Exception:
            logger.exception("LLMService generate call failed")
            raise

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Return a conversational response for a list of chat messages.
        Format expected: [{"role": "user"|"system"|"assistant", "content": "..."}]
        """
        if not messages:
            logger.warning("Empty messages list passed to LLMService.chat().")
            return ""

        try:
            logger.info(f"Sending chat request to Ollama ({self.model_name})...")
            response = self.client.chat(
                model=self.model_name,
                messages=messages
            )
            
            text = response.get("message", {}).get("content", "").strip()

            if not text:
                logger.warning("Ollama returned an empty chat response.")
                return "The language model returned an empty response."

            return text

        except Exception:
            logger.exception("LLMService chat call failed")
            raise


# Singleton instance for application-wide imports
llm_service = LLMService()