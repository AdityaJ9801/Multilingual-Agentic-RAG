"""Vector database service using Qdrant."""
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config import get_settings
from app.utils.logger import get_logger
from app.models import DocumentChunk, DocumentMetadata

logger = get_logger(__name__)

# Global Qdrant client instance
_qdrant_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    """Get or initialize the Qdrant client."""
    global _qdrant_client
    
    if _qdrant_client is None:
        settings = get_settings()
        logger.info(f"Connecting to Qdrant at {settings.qdrant_host}:{settings.qdrant_port}")
        
        _qdrant_client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
            timeout=settings.qdrant_timeout
        )
        
        logger.info("Connected to Qdrant successfully")
    
    return _qdrant_client


def ensure_collection_exists() -> None:
    """Ensure the collection exists, create if not."""
    settings = get_settings()
    client = get_qdrant_client()
    
    try:
        # Check if collection exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]
        
        if settings.qdrant_collection_name not in collection_names:
            logger.info(f"Creating collection: {settings.qdrant_collection_name}")
            
            client.create_collection(
                collection_name=settings.qdrant_collection_name,
                vectors_config=VectorParams(
                    size=settings.qdrant_vector_size,
                    distance=Distance.COSINE
                )
            )
            
            logger.info(f"Collection created: {settings.qdrant_collection_name}")
        else:
            logger.info(f"Collection already exists: {settings.qdrant_collection_name}")
            
    except Exception as e:
        logger.error(f"Error ensuring collection exists: {e}")
        raise


def add_documents(documents: List[DocumentChunk]) -> None:
    """
    Add documents to the vector database.
    
    Args:
        documents: List of document chunks to add
    """
    if not documents:
        return
    
    settings = get_settings()
    client = get_qdrant_client()
    
    ensure_collection_exists()
    
    # Prepare points for insertion
    points = []
    for i, doc in enumerate(documents):
        if not doc.embedding:
            logger.warning(f"Document {doc.id} has no embedding, skipping")
            continue
        
        point = PointStruct(
            id=hash(doc.id) % (2**31),  # Convert string ID to positive integer
            vector=doc.embedding,
            payload={
                "id": doc.id,
                "content": doc.content,
                "source": doc.metadata.source,
                "file_type": doc.metadata.file_type,
                "language": doc.metadata.language,
                "chunk_index": doc.metadata.chunk_index,
                "total_chunks": doc.metadata.total_chunks,
                "page_number": doc.metadata.page_number,
                "timestamp": doc.metadata.timestamp.isoformat(),
                "original_filename": doc.metadata.original_filename,
            }
        )
        points.append(point)
    
    if points:
        logger.info(f"Adding {len(points)} points to Qdrant")
        client.upsert(
            collection_name=settings.qdrant_collection_name,
            points=points
        )
        logger.info(f"Successfully added {len(points)} points")


def search_documents(
    query_embedding: List[float],
    top_k: int = 5,
    language_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for documents similar to the query embedding.
    
    Args:
        query_embedding: Query embedding vector
        top_k: Number of results to return
        language_filter: Optional language filter
        
    Returns:
        List of search results
    """
    settings = get_settings()
    client = get_qdrant_client()
    
    ensure_collection_exists()
    
    try:
        # Build query filter if language is specified
        query_filter = None
        if language_filter:
            query_filter = {
                "must": [
                    {
                        "key": "language",
                        "match": {"value": language_filter}
                    }
                ]
            }
        
        # Search
        results = client.search(
            collection_name=settings.qdrant_collection_name,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.payload.get("id"),
                "content": result.payload.get("content"),
                "score": result.score,
                "metadata": {
                    "source": result.payload.get("source"),
                    "file_type": result.payload.get("file_type"),
                    "language": result.payload.get("language") or language_filter or "en",
                    "chunk_index": result.payload.get("chunk_index"),
                    "page_number": result.payload.get("page_number"),
                    "original_filename": result.payload.get("original_filename"),
                }
            })
        
        logger.debug(f"Found {len(formatted_results)} results")
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise


def delete_collection() -> None:
    """Delete the collection (for cleanup/testing)."""
    settings = get_settings()
    client = get_qdrant_client()
    
    try:
        client.delete_collection(collection_name=settings.qdrant_collection_name)
        logger.info(f"Deleted collection: {settings.qdrant_collection_name}")
    except Exception as e:
        logger.error(f"Error deleting collection: {e}")
        raise


def get_collection_info() -> Dict[str, Any]:
    """Get information about the collection."""
    settings = get_settings()
    client = get_qdrant_client()
    
    try:
        collection_info = client.get_collection(settings.qdrant_collection_name)
        return {
            "name": settings.qdrant_collection_name,
            "points_count": collection_info.points_count,
            "vectors_count": collection_info.vectors_count,
        }
    except Exception as e:
        logger.error(f"Error getting collection info: {e}")
        return {}

