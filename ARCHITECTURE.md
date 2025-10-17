# Architecture Documentation

## System Overview

The Multilingual Agentic RAG system is built on a microservices architecture with specialized agents for different tasks.

## Core Components

### 1. API Gateway (FastAPI)
- **Purpose**: REST API interface for all client interactions
- **Responsibilities**:
  - Request validation and routing
  - Response formatting
  - Rate limiting and authentication
  - CORS handling
- **Port**: 8000

### 2. Agent Orchestrator
- **Purpose**: Coordinates agent collaboration
- **Pattern**: Pipeline orchestration with message passing
- **Flow**:
  1. Router Agent analyzes query
  2. Retrieval Agent fetches documents
  3. Synthesis Agent generates response
  4. Validation Agent verifies response (optional)

### 3. Specialized Agents

#### Router Agent
- **Input**: User query
- **Output**: Routing decision with target agents
- **Logic**:
  - Analyzes query type (factual, explanatory, summarization, general)
  - Determines required agents
  - Detects query language
  - Sets processing priority

#### Retrieval Agent
- **Input**: Query and language
- **Output**: Relevant documents
- **Process**:
  1. Generate query embedding
  2. Search vector database
  3. Filter by language (optional)
  4. Return top-k results with scores

#### Synthesis Agent
- **Input**: Query and retrieved documents
- **Output**: Generated response
- **Process**:
  1. Build context from documents
  2. Create language-specific prompt
  3. Call LLM for generation
  4. Extract sources and confidence

#### Validation Agent
- **Input**: Response and source documents
- **Output**: Validation result
- **Checks**:
  - Response quality (length, completeness)
  - Citation verification
  - Fact-checking against sources
  - Confidence scoring

### 4. Vector Database (Qdrant)
- **Purpose**: Store and search document embeddings
- **Configuration**:
  - Distance Metric: Cosine Similarity
  - Index Type: HNSW (Hierarchical Navigable Small World)
  - Vector Size: 384 (multilingual-e5-large)
- **Operations**:
  - Upsert: Add/update documents
  - Search: Find similar documents
  - Filter: Language-based filtering

### 5. LLM Service (Ollama)
- **Purpose**: Local LLM inference
- **Supported Models**:
  - Mistral (7B) - Recommended
  - Llama 2 (7B, 13B)
  - Mixtral (8x7B)
  - Qwen2 (7B, 14B)
- **Configuration**:
  - Temperature: 0.7 (default)
  - Top-p: 0.9 (default)
  - Max tokens: 2048 (default)

### 6. Embedding Model
- **Model**: sentence-transformers/multilingual-e5-large
- **Capabilities**:
  - 384-dimensional vectors
  - Supports 100+ languages
  - Optimized for semantic search
- **Performance**: ~1000 texts/minute on CPU

## Data Flow

### Document Ingestion Flow
```
User Upload
    ↓
File Validation
    ↓
Text Extraction (PDF/TXT/MD/JSON/CSV)
    ↓
Language Detection
    ↓
Text Chunking (512 chars, 10% overlap)
    ↓
Embedding Generation
    ↓
Vector Database Storage
    ↓
Metadata Storage
    ↓
Success Response
```

### Query Processing Flow
```
User Query
    ↓
Language Detection
    ↓
Router Agent (Routing Decision)
    ↓
Retrieval Agent (Vector Search)
    ↓
Synthesis Agent (LLM Generation)
    ↓
Validation Agent (Fact-Checking)
    ↓
Response Formatting
    ↓
Client Response
```

## Multilingual Support

### Language Detection
- Uses `langdetect` library
- Confidence threshold: 0.5 (configurable)
- Fallback to default language if confidence too low

### Multilingual Embeddings
- Model: multilingual-e5-large
- Supports 100+ languages
- Language-specific filtering in vector search

### Response Generation
- Prompts include language specification
- LLM generates responses in query language
- Maintains language consistency

## Scalability Strategies

### Horizontal Scaling
1. **Stateless API**: Multiple API instances behind load balancer
2. **Vector Database**: Qdrant supports clustering
3. **LLM Service**: Multiple Ollama instances with load balancing

### Vertical Scaling
1. **Larger Models**: Use 13B or 70B models on high-end hardware
2. **GPU Acceleration**: Enable CUDA for Ollama and embeddings
3. **Batch Processing**: Increase embedding batch size

### Performance Optimization
1. **Caching**: Cache embeddings and frequent queries
2. **Connection Pooling**: Reuse database connections
3. **Async Processing**: Non-blocking I/O for all services
4. **Model Quantization**: Use quantized models for faster inference

## Error Handling

### Retry Logic
- Ollama calls: 3 retries with exponential backoff
- Vector DB: Automatic reconnection
- Embedding generation: Batch retry with fallback

### Graceful Degradation
- Missing documents: Return empty results
- LLM timeout: Return cached response or error
- Validation failure: Still return response with lower confidence

## Security

### Authentication
- API key validation on all endpoints
- JWT token support (optional)
- Rate limiting per API key

### Data Protection
- Encrypted connections (HTTPS in production)
- Non-root Docker containers
- Secrets management via environment variables

### Input Validation
- File type validation
- File size limits
- Query length limits
- Pydantic model validation

## Monitoring & Logging

### Structured Logging
- JSON format for log aggregation
- Log levels: DEBUG, INFO, WARNING, ERROR
- Contextual information in all logs

### Health Checks
- API health endpoint
- Service dependency checks
- Vector database status
- LLM availability

### Metrics
- Query processing time
- Document ingestion rate
- Agent processing times
- Error rates

## Configuration Management

### Environment Variables
- Service URLs and credentials
- Model parameters
- Language settings
- Feature flags

### Configuration Validation
- Startup validation of all settings
- Type checking with Pydantic
- Default values for optional settings

## Deployment Considerations

### Docker Compose
- Service dependencies and startup order
- Volume mounts for persistent data
- Network isolation
- Resource limits

### Production Deployment
- Use managed services (Qdrant Cloud, etc.)
- Implement load balancing
- Set up monitoring and alerting
- Configure backup and recovery

## Future Enhancements

1. **Advanced Caching**: Redis for query/embedding caching
2. **Hybrid Search**: Combine vector and keyword search
3. **Multi-turn Conversations**: Maintain context across queries
4. **Fine-tuning**: Custom model fine-tuning
5. **Knowledge Graphs**: Structured knowledge representation
6. **Real-time Updates**: Streaming responses

