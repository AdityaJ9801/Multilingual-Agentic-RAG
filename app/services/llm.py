"""LLM service using Ollama."""
from typing import Optional, Dict, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """Client for interacting with Ollama."""
    
    def __init__(self):
        """Initialize Ollama client."""
        self.settings = get_settings()
        self.base_url = self.settings.ollama_base_url
        self.model = self.settings.ollama_model
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate text using Ollama.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        temperature = temperature or self.settings.ollama_temperature
        top_p = top_p or self.settings.ollama_top_p
        max_tokens = max_tokens or self.settings.ollama_max_tokens
        
        try:
            logger.debug(f"Generating text with model: {self.model}")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "top_p": top_p,
                    "num_predict": max_tokens,
                    "stream": False,
                },
                timeout=self.settings.ollama_timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            generated_text = result.get("response", "").strip()
            logger.debug(f"Generated {len(generated_text)} characters")
            
            return generated_text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in LLM generation: {e}")
            raise
    
    def check_health(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False
    
    def list_models(self) -> list:
        """List available models in Ollama."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []


# Global Ollama client instance
_ollama_client: OllamaClient | None = None


def get_ollama_client() -> OllamaClient:
    """Get or initialize the Ollama client."""
    global _ollama_client
    
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    
    return _ollama_client


def generate_text(
    prompt: str,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> str:
    """
    Generate text using the LLM.
    
    Args:
        prompt: Input prompt
        temperature: Sampling temperature
        top_p: Top-p sampling parameter
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated text
    """
    client = get_ollama_client()
    return client.generate(
        prompt=prompt,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )

