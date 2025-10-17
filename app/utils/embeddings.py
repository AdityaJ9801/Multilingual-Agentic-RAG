"""Embedding generation utilities."""
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Global embedding model instance
_embedding_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Get or initialize the embedding model."""
    global _embedding_model
    
    if _embedding_model is None:
        settings = get_settings()
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        _embedding_model = SentenceTransformer(
            settings.embedding_model,
            device=settings.embedding_device
        )
        logger.info("Embedding model loaded successfully")
    
    return _embedding_model


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    if not texts:
        return []
    
    settings = get_settings()
    model = get_embedding_model()
    
    logger.debug(f"Generating embeddings for {len(texts)} texts")
    
    # Generate embeddings with batching
    embeddings = model.encode(
        texts,
        batch_size=settings.embedding_batch_size,
        convert_to_numpy=True,
        show_progress_bar=False
    )
    
    # Convert to list of lists
    if isinstance(embeddings, np.ndarray):
        embeddings = embeddings.tolist()
    
    logger.debug(f"Generated {len(embeddings)} embeddings")
    return embeddings


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text.
    
    Args:
        text: Text to embed
        
    Returns:
        Embedding vector
    """
    embeddings = generate_embeddings([text])
    return embeddings[0] if embeddings else []


def get_embedding_dimension() -> int:
    """Get the dimension of the embedding vectors."""
    model = get_embedding_model()
    return model.get_sentence_embedding_dimension()

