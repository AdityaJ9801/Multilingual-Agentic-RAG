"""API routes for the RAG system."""
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from datetime import datetime
import uuid
import time

from app.models import (
    QueryRequest, QueryResponse, IngestionRequest, IngestionResponse,
    DocumentListResponse, DocumentInfo, HealthCheckResponse, AgentsStatusResponse
)
from app.services.document_processor import process_document
from app.services.vector_db import add_documents, get_collection_info
from app.agents.orchestrator import get_orchestrator
from app.services.llm import get_ollama_client
from app.utils.logger import get_logger
from app.config import get_settings

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1", tags=["RAG"])

# In-memory document store (in production, use a database)
_documents_store = {}


@router.post("/ingest", response_model=IngestionResponse)
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingest and process a document.
    
    Supported formats: PDF, TXT, MD, JSON, CSV
    """
    try:
        settings = get_settings()
        
        # Validate file type
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in settings.supported_file_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}"
            )
        
        # Read file content
        content = await file.read()
        
        # Validate file size
        file_size_mb = len(content) / (1024 * 1024)
        if file_size_mb > settings.max_file_size_mb:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {settings.max_file_size_mb}MB"
            )
        
        logger.info(f"Processing file: {file.filename} ({file_size_mb:.2f}MB)")
        
        # Process document
        document_chunks = process_document(
            file_name=file.filename,
            file_type=file_ext,
            file_content=content
        )
        
        # Add to vector database
        add_documents(document_chunks)
        
        # Store document info
        document_id = str(uuid.uuid4())
        _documents_store[document_id] = {
            "file_name": file.filename,
            "file_type": file_ext,
            "chunks_count": len(document_chunks),
            "language": document_chunks[0].metadata.language if document_chunks else "unknown",
            "ingestion_date": datetime.utcnow(),
            "file_size_bytes": len(content)
        }
        
        return IngestionResponse(
            document_id=document_id,
            file_name=file.filename,
            chunks_created=len(document_chunks),
            language=document_chunks[0].metadata.language if document_chunks else "unknown",
            status="success",
            message=f"Successfully ingested {len(document_chunks)} chunks"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Submit a query and get a RAG response.
    """
    try:
        start_time = time.time()
        
        logger.info(f"Processing query: {request.query[:100]}...")
        
        # Get orchestrator
        orchestrator = get_orchestrator()
        
        # Process query through agents
        result = await orchestrator.process_query(
            query=request.query,
            language=request.language,
            top_k=request.top_k,
            include_validation=True
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Query processing failed")
            )
        
        # Format response
        sources = []
        if request.include_sources:
            sources = [
                {
                    "source": source,
                    "type": "document"
                }
                for source in result.get("sources", [])
            ]
        
        reasoning = None
        if request.include_reasoning:
            reasoning = str(result.get("agent_states", {}))
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        return QueryResponse(
            query=request.query,
            language=result.get("language", "en"),
            response=result.get("response", ""),
            sources=sources,
            reasoning=reasoning,
            confidence=result.get("confidence", 0.0),
            processing_time_ms=processing_time_ms,
            agent_states=result.get("agent_states")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    """List all ingested documents."""
    try:
        documents = [
            DocumentInfo(
                document_id=doc_id,
                file_name=doc_info["file_name"],
                file_type=doc_info["file_type"],
                language=doc_info["language"],
                chunks_count=doc_info["chunks_count"],
                ingestion_date=doc_info["ingestion_date"],
                file_size_bytes=doc_info["file_size_bytes"]
            )
            for doc_id, doc_info in _documents_store.items()
        ]
        
        return DocumentListResponse(
            documents=documents,
            total_count=len(documents)
        )
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document."""
    try:
        if document_id not in _documents_store:
            raise HTTPException(status_code=404, detail="Document not found")
        
        del _documents_store[document_id]
        
        return {
            "status": "success",
            "message": f"Document {document_id} deleted"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    try:
        settings = get_settings()
        ollama_client = get_ollama_client()
        
        # Check Ollama
        ollama_healthy = ollama_client.check_health()
        
        # Check Qdrant
        try:
            collection_info = get_collection_info()
            qdrant_healthy = True
        except:
            qdrant_healthy = False
            collection_info = {}
        
        services = {
            "ollama": {
                "status": "healthy" if ollama_healthy else "unhealthy",
                "model": settings.ollama_model
            },
            "qdrant": {
                "status": "healthy" if qdrant_healthy else "unhealthy",
                "collection_info": collection_info
            }
        }
        
        overall_status = "healthy" if (ollama_healthy and qdrant_healthy) else "degraded"
        
        return HealthCheckResponse(
            status=overall_status,
            timestamp=datetime.utcnow(),
            services=services,
            version=settings.app_version
        )
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/status")
async def agents_status():
    """Get status of all agents."""
    try:
        orchestrator = get_orchestrator()
        agents_status = orchestrator.get_agents_status()
        
        return AgentsStatusResponse(
            agents=agents_status,
            overall_status="operational",
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error getting agents status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

