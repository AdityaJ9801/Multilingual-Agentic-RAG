# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints require an API key in the header:
```
X-API-Key: your-api-key
```

## Endpoints

### 1. Ingest Document
**POST** `/ingest`

Upload and process a document for ingestion into the knowledge base.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (binary) - Document file

**Supported Formats:**
- PDF (.pdf)
- Text (.txt)
- Markdown (.md)
- JSON (.json)
- CSV (.csv)

**Response:**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "file_name": "document.pdf",
  "chunks_created": 42,
  "language": "en",
  "status": "success",
  "message": "Successfully ingested 42 chunks"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "X-API-Key: your-api-key" \
  -F "file=@document.pdf"
```

**Error Responses:**
- 400: Unsupported file type
- 413: File too large (>50MB)
- 500: Processing error

---

### 2. Query
**POST** `/query`

Submit a query and receive a RAG-generated response.

**Request:**
```json
{
  "query": "What is machine learning?",
  "language": "en",
  "top_k": 5,
  "include_sources": true,
  "include_reasoning": false
}
```

**Parameters:**
- `query` (string, required): User query (1-5000 chars)
- `language` (string, optional): Language code (en, es, fr, zh, ar). Auto-detected if not provided
- `top_k` (integer, optional): Number of documents to retrieve (1-50, default: 5)
- `include_sources` (boolean, optional): Include source documents (default: true)
- `include_reasoning` (boolean, optional): Include agent reasoning (default: false)

**Response:**
```json
{
  "query": "What is machine learning?",
  "language": "en",
  "response": "Machine learning is a subset of artificial intelligence...",
  "sources": [
    {
      "source": "document.pdf",
      "type": "document"
    }
  ],
  "reasoning": null,
  "confidence": 0.85,
  "processing_time_ms": 2345.67,
  "agent_states": {
    "router": {
      "agent_name": "router",
      "status": "idle",
      "processed_queries": 1,
      "error_count": 0
    }
  }
}
```

**Examples:**

English Query:
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 5,
    "include_sources": true
  }'
```

Spanish Query:
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Qué es el aprendizaje automático?",
    "top_k": 5
  }'
```

French Query:
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Qu'\''est-ce que l'\''apprentissage automatique?",
    "top_k": 5
  }'
```

Chinese Query:
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "什么是机器学习?",
    "top_k": 5
  }'
```

Arabic Query:
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ما هو التعلم الآلي؟",
    "top_k": 5
  }'
```

---

### 3. List Documents
**GET** `/documents`

Retrieve a list of all ingested documents.

**Response:**
```json
{
  "documents": [
    {
      "document_id": "550e8400-e29b-41d4-a716-446655440000",
      "file_name": "document.pdf",
      "file_type": "pdf",
      "language": "en",
      "chunks_count": 42,
      "ingestion_date": "2024-01-15T10:30:00",
      "file_size_bytes": 1024000
    }
  ],
  "total_count": 1
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/documents" \
  -H "X-API-Key: your-api-key"
```

---

### 4. Delete Document
**DELETE** `/documents/{document_id}`

Remove a document from the knowledge base.

**Parameters:**
- `document_id` (string, path): Document ID to delete

**Response:**
```json
{
  "status": "success",
  "message": "Document 550e8400-e29b-41d4-a716-446655440000 deleted"
}
```

**Example:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/documents/550e8400-e29b-41d4-a716-446655440000" \
  -H "X-API-Key: your-api-key"
```

---

### 5. Health Check
**GET** `/health`

Check the health status of all services.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "services": {
    "ollama": {
      "status": "healthy",
      "model": "mistral"
    },
    "qdrant": {
      "status": "healthy",
      "collection_info": {
        "name": "documents",
        "points_count": 42,
        "vectors_count": 42
      }
    }
  },
  "version": "1.0.0"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/health" \
  -H "X-API-Key: your-api-key"
```

---

### 6. Agent Status
**GET** `/agents/status`

Get the status of all agents.

**Response:**
```json
{
  "agents": [
    {
      "agent_name": "router",
      "status": "idle",
      "current_task": null,
      "last_update": "2024-01-15T10:30:00",
      "processed_queries": 5,
      "error_count": 0
    }
  ],
  "overall_status": "operational",
  "timestamp": "2024-01-15T10:30:00"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/agents/status" \
  -H "X-API-Key: your-api-key"
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes
- 200: Success
- 400: Bad request (validation error)
- 404: Not found
- 413: Payload too large
- 429: Rate limit exceeded
- 500: Internal server error

---

## Rate Limiting

Default rate limits:
- 100 requests per 60 seconds per API key

Response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705318200
```

---

## Pagination

Currently not implemented. Use `top_k` parameter in query endpoint to limit results.

---

## Versioning

Current API version: `v1`

Future versions will be available at `/api/v2`, etc.

