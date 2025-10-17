"""Retrieval agent for document retrieval."""
from typing import Dict, Any
import time
from app.agents.base import BaseAgent
from app.models import AgentMessage, RetrievalResult
from app.utils.logger import get_logger
from app.utils.embeddings import generate_embedding
from app.services.vector_db import search_documents

logger = get_logger(__name__)


class RetrievalAgent(BaseAgent):
    """Retrieves relevant documents from the knowledge base."""
    
    def __init__(self):
        """Initialize retrieval agent."""
        super().__init__("retrieval")
    
    async def process(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Retrieve documents relevant to the query.
        
        Args:
            message: Input message containing query
            
        Returns:
            Retrieval result
        """
        self.update_status("processing", "retrieving_documents")
        start_time = time.time()
        
        try:
            query = message.content.get("query", "")
            language = message.content.get("language", "en")
            top_k = message.content.get("top_k", 5)
            
            logger.info(f"Retrieving documents for query: {query[:100]}...")
            
            # Generate embedding for query
            query_embedding = generate_embedding(query)
            
            # Search documents
            search_results = search_documents(
                query_embedding=query_embedding,
                top_k=top_k,
                language_filter=language
            )
            
            # Format results
            documents = []
            for result in search_results:
                from app.models import DocumentChunk, DocumentMetadata
                from datetime import datetime
                
                metadata = DocumentMetadata(
                    source=result["metadata"].get("source", "unknown"),
                    file_type=result["metadata"].get("file_type", "unknown"),
                    language=result["metadata"].get("language") or "en",
                    chunk_index=result["metadata"].get("chunk_index", 0),
                    total_chunks=result["metadata"].get("total_chunks", 1),
                    page_number=result["metadata"].get("page_number"),
                    timestamp=datetime.utcnow(),
                    original_filename=result["metadata"].get("original_filename")
                )
                
                doc = DocumentChunk(
                    id=result["id"],
                    content=result["content"],
                    metadata=metadata
                )
                documents.append(doc)
            
            retrieval_time_ms = (time.time() - start_time) * 1000
            
            retrieval_result = RetrievalResult(
                documents=documents,
                query=query,
                language=language,
                retrieval_time_ms=retrieval_time_ms,
                total_results=len(documents)
            )
            
            self.update_status("idle")
            self.increment_processed_queries()
            
            logger.info(f"Retrieved {len(documents)} documents in {retrieval_time_ms:.2f}ms")
            
            return {
                "retrieval_result": retrieval_result.model_dump(),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error in retrieval agent: {e}")
            self.increment_error_count()
            self.update_status("error")
            return {
                "success": False,
                "error": str(e)
            }

