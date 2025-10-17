"""Data models for the RAG system."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# ============================================================================
# Request/Response Models
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str = Field(..., min_length=1, max_length=5000, description="User query")
    language: Optional[str] = Field(None, description="Query language (auto-detected if not provided)")
    top_k: int = Field(5, ge=1, le=50, description="Number of documents to retrieve")
    include_sources: bool = Field(True, description="Include source documents in response")
    include_reasoning: bool = Field(False, description="Include agent reasoning in response")


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    query: str
    language: str
    response: str
    sources: List[Dict[str, Any]] = []
    reasoning: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time_ms: float
    agent_states: Optional[Dict[str, Any]] = None


class DocumentMetadata(BaseModel):
    """Metadata for ingested documents."""
    source: str
    file_type: str
    language: str
    chunk_index: int
    total_chunks: int
    page_number: Optional[int] = None
    timestamp: datetime
    original_filename: Optional[str] = None


class DocumentChunk(BaseModel):
    """A chunk of a document."""
    id: str
    content: str
    metadata: DocumentMetadata
    embedding: Optional[List[float]] = None


class IngestionRequest(BaseModel):
    """Request model for document ingestion."""
    file_name: str
    file_type: str
    content: str
    language: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class IngestionResponse(BaseModel):
    """Response model for ingestion endpoint."""
    document_id: str
    file_name: str
    chunks_created: int
    language: str
    status: str
    message: str


class DocumentInfo(BaseModel):
    """Information about an ingested document."""
    document_id: str
    file_name: str
    file_type: str
    language: str
    chunks_count: int
    ingestion_date: datetime
    file_size_bytes: int


class DocumentListResponse(BaseModel):
    """Response for listing documents."""
    documents: List[DocumentInfo]
    total_count: int


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    services: Dict[str, Dict[str, Any]]
    version: str


class AgentStatusResponse(BaseModel):
    """Agent status response."""
    agent_name: str
    status: str
    last_activity: Optional[datetime] = None
    processed_queries: int = 0
    error_count: int = 0


class AgentsStatusResponse(BaseModel):
    """Response for agents status endpoint."""
    agents: List[AgentStatusResponse]
    overall_status: str
    timestamp: datetime


# ============================================================================
# Internal Models
# ============================================================================

class AgentMessage(BaseModel):
    """Message passed between agents."""
    sender: str
    receiver: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentState(BaseModel):
    """State of an agent."""
    agent_name: str
    status: str  # idle, processing, error
    current_task: Optional[str] = None
    last_update: datetime = Field(default_factory=datetime.utcnow)
    metrics: Dict[str, Any] = {}


class RetrievalResult(BaseModel):
    """Result from retrieval agent."""
    documents: List[DocumentChunk]
    query: str
    language: str
    retrieval_time_ms: float
    total_results: int


class SynthesisResult(BaseModel):
    """Result from synthesis agent."""
    response: str
    sources: List[str]
    confidence: float
    synthesis_time_ms: float


class ValidationResult(BaseModel):
    """Result from validation agent."""
    is_valid: bool
    confidence: float
    issues: List[str] = []
    suggestions: List[str] = []
    validation_time_ms: float


class RoutingDecision(BaseModel):
    """Decision from router agent."""
    query_type: str
    target_agents: List[str]
    priority: int
    requires_retrieval: bool
    requires_validation: bool
    language: str

