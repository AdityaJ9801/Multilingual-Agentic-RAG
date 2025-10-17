# 📦 Installation Guide - Multilingual Agentic RAG System

## 🎯 Overview

This guide provides step-by-step instructions to install and run the **Multilingual Agentic RAG System** with a Streamlit frontend.

**System Features:**
- ✅ Multilingual support (English, Spanish, French, Chinese, Arabic)
- ✅ FastAPI REST backend
- ✅ Streamlit web interface
- ✅ Vector database (Qdrant)
- ✅ Local LLM inference (Ollama)
- ✅ Docker containerization

---

## 📋 Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 8GB minimum (16GB recommended)
- **Disk Space**: 20GB minimum
- **Docker**: Latest version installed
- **Python**: 3.9+ (for local development)

### Required Software
1. **Docker Desktop** - https://www.docker.com/products/docker-desktop
2. **Git** - https://git-scm.com/
3. **Python 3.9+** - https://www.python.org/

---

## 🚀 Installation Steps

### Step 1: Clone or Download the Project

```bash
# Clone the repository
git clone <repository-url>
cd multi_agentic_rag

# Or extract the provided ZIP file
unzip multi_agentic_rag.zip
cd multi_agentic_rag
```

### Step 2: Verify Project Structure

```bash
# Check if all required files exist
ls -la

# You should see:
# - app/                    (Application code)
# - scripts/                (Helper scripts)
# - sample_data/            (Sample documents)
# - docker-compose.yml      (Docker configuration)
# - requirements.txt        (Python dependencies)
# - streamlit_app.py        (Streamlit frontend)
# - streamlit_requirements.txt
# - README.md
# - ARCHITECTURE.md
```

### Step 3: Start Docker Services

```bash
# Start all services (API, Ollama, Qdrant)
docker-compose up -d

# Verify services are running
docker-compose ps

# Expected output:
# NAME                COMMAND                  STATUS
# qdrant              "/qdrant/qdrant ..."     Up
# ollama              "/bin/sh -c 'ollama..."  Up
# api                 "python -m uvicorn..."   Up
```

### Step 4: Wait for Services to Initialize

```bash
# Wait 30-60 seconds for services to fully start
sleep 60

# Check API health
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"healthy","version":"1.0.0"}
```

### Step 5: Ingest Sample Data

```bash
# Run the data ingestion script
bash scripts/ingest_sample_data.sh

# Or on Windows:
# python scripts/test_multilingual_python.py

# This will:
# - Load sample documents
# - Create embeddings
# - Store in vector database
```

### Step 6: Install Streamlit Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Streamlit dependencies
pip install -r streamlit_requirements.txt
```

### Step 7: Start Streamlit Application

```bash
# Run Streamlit app
streamlit run streamlit_app.py

# Expected output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://<your-ip>:8501
```

### Step 8: Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

---

## 🧪 Verification

### Test 1: Check API Health

```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response:**
```json
{"status":"healthy","version":"1.0.0"}
```

### Test 2: Run a Query

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is artificial intelligence?",
    "language": "en",
    "top_k": 5,
    "include_sources": true,
    "include_reasoning": false
  }'
```

**Expected Response:**
```json
{
  "query": "What is artificial intelligence?",
  "language": "en",
  "response": "Artificial Intelligence (AI) is...",
  "confidence": 0.6,
  "processing_time_ms": 22071.70,
  "sources": [...]
}
```

### Test 3: Use Streamlit Interface

1. Open http://localhost:8501
2. Go to **Query** tab
3. Enter a query in any language
4. Click **Submit**
5. ✅ Should see response without errors

---

## 📁 Project Structure

```
multi_agentic_rag/
├── app/                          # Application code
│   ├── agents/                   # Agent implementations
│   │   ├── router.py
│   │   ├── retrieval.py
│   │   ├── synthesis.py
│   │   ├── validation.py
│   │   └── orchestrator.py
│   ├── api/                      # FastAPI routes
│   │   └── routes.py
│   ├── services/                 # Business logic
│   │   ├── vector_db.py
│   │   ├── document_processor.py
│   │   └── llm_service.py
│   ├── models.py                 # Pydantic models
│   ├── config.py                 # Configuration
│   └── main.py                   # FastAPI app
├── scripts/                      # Helper scripts
│   ├── setup.sh
│   ├── health_check.sh
│   ├── ingest_sample_data.sh
│   └── test_multilingual_python.py
├── sample_data/                  # Sample documents
│   ├── machine_learning_en.txt
│   ├── machine_learning_es.txt
│   └── machine_learning_fr.txt
├── streamlit_app.py              # Streamlit frontend
├── docker-compose.yml            # Docker configuration
├── requirements.txt              # Python dependencies
├── streamlit_requirements.txt     # Streamlit dependencies
├── README.md                      # Project overview
├── ARCHITECTURE.md               # System architecture
└── API_DOCS.md                   # API documentation
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_LOG_LEVEL=info

# Ollama Configuration
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=mistral

# Qdrant Configuration
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=documents

# Application Configuration
EMBEDDING_MODEL=mistral
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=5
```

---

## 🛑 Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# View logs
docker-compose logs -f api

# Restart services
docker-compose restart
```

---

## 🐛 Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Issue: Services Not Starting

```bash
# Check Docker status
docker-compose ps

# View logs
docker-compose logs

# Restart services
docker-compose restart
```

### Issue: Streamlit Connection Error

```bash
# Verify API is running
curl http://localhost:8000/api/v1/health

# Check Streamlit logs
# Look at terminal where streamlit is running
```

### Issue: No Documents Found

```bash
# Re-ingest sample data
bash scripts/ingest_sample_data.sh

# Or manually upload documents via Streamlit UI
```

---

## 📚 Documentation

- **README.md** - Project overview
- **ARCHITECTURE.md** - System architecture
- **API_DOCS.md** - API documentation
- **INDEX.md** - File index

---

## 🎯 Next Steps

1. ✅ Complete installation
2. ✅ Verify all services running
3. ✅ Test API endpoints
4. ✅ Use Streamlit interface
5. ✅ Upload your own documents
6. ✅ Query in multiple languages

---

## 📞 Support

For issues or questions:

1. Check **ARCHITECTURE.md** for system design
2. Review **API_DOCS.md** for API details
3. Check Docker logs: `docker-compose logs`
4. Verify services: `docker-compose ps`

---

**Status**: ✅ Ready to Install  
**Version**: 1.0.0  
**Last Updated**: October 17, 2025

🎉 **Follow these steps to get started!**

