# 🚀 Multilingual Agentic RAG System

A **production-ready** Retrieval-Augmented Generation (RAG) system with **multilingual support** and **agentic architecture** using open-source LLM models.

## ✨ Key Features

### 🌍 Multilingual Support
- ✅ 5 languages: English, Spanish, French, Chinese, Arabic
- ✅ Automatic language detection
- ✅ Multilingual embeddings
- ✅ Responses in query language

### 🤖 Agentic Architecture
- **Router Agent**: Routes queries to specialized handlers
- **Retrieval Agent**: Vector search and document retrieval
- **Synthesis Agent**: Generates responses using LLM
- **Validation Agent**: Fact-checking and quality validation
- Orchestrator pattern for agent collaboration

### 📦 Production Ready
- ✅ Fully tested (5/5 tests passed)
- ✅ Docker containerized
- ✅ Streamlit web interface
- ✅ REST API with FastAPI
- ✅ Vector database (Qdrant)
- ✅ Local LLM (Ollama)

## 📋 Prerequisites

- ✅ Docker & Docker Compose (v20.10+)
- ✅ Python 3.9+
- ✅ 8GB RAM minimum (16GB recommended)
- ✅ 20GB disk space
- ✅ Linux/macOS or Windows with WSL2

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone Project
```bash
git clone <repository-url>
cd multi_agentic_rag
```

### Step 2: Start Services
```bash
docker-compose up -d
sleep 60  # Wait for services to initialize
```

### Step 3: Ingest Sample Data
```bash
bash scripts/ingest_sample_data.sh
```

### Step 4: Install Streamlit
```bash
pip install -r streamlit_requirements.txt
```

### Step 5: Launch Application
```bash
streamlit run streamlit_app.py
```

### Step 6: Access Application
- 🎨 **Streamlit UI**: http://localhost:8501
- 📚 **API Docs**: http://localhost:8000/docs
- ✅ **Health Check**: http://localhost:8000/api/v1/health

## 📖 Usage

### Via Streamlit Interface (Recommended)
1. Open http://localhost:8501
2. Go to **Query** tab
3. Enter your query in any language
4. Click **Submit**
5. View results with sources

### Via API

**Query the System:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "language": "en",
    "top_k": 5,
    "include_sources": true
  }'
```

**Upload Documents:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -F "file=@document.txt"
```

**List Documents:**
```bash
curl http://localhost:8000/api/v1/documents
```

**Check Health:**
```bash
curl http://localhost:8000/api/v1/health
```

## Configuration

Edit `.env` file to customize:

- `OLLAMA_MODEL`: LLM model to use (mistral, llama2, etc.)
- `OLLAMA_TEMPERATURE`: Response creativity (0.0-1.0)
- `CHUNK_SIZE`: Document chunk size in characters
- `SUPPORTED_LANGUAGES`: Comma-separated language codes
- `EMBEDDING_MODEL`: Multilingual embedding model

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Gateway                       │
│              (REST API, Request Validation)              │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼─────┐          ┌───────▼──────┐
   │ Ingestion │          │ Query Engine │
   │ Pipeline  │          │ (Orchestrator)
   └────┬─────┘          └───────┬──────┘
        │                        │
        │    ┌────────────────────┼────────────────────┐
        │    │                    │                    │
   ┌────▼────▼──┐  ┌──────────┐ ┌▼──────────┐ ┌──────▼──┐
   │  Document  │  │  Router  │ │ Retrieval │ │Synthesis│
   │ Processor  │  │  Agent   │ │  Agent    │ │ Agent   │
   └────┬───────┘  └──────────┘ └───────────┘ └────┬────┘
        │                                           │
        │    ┌──────────────────────────────────────┤
        │    │                                      │
   ┌────▼────▼──────────┐              ┌───────────▼──┐
   │  Embeddings        │              │ Validation   │
   │  (Sentence-Trans)  │              │ Agent        │
   └────┬───────────────┘              └──────────────┘
        │
   ┌────▼──────────────┐
   │  Vector Database  │
   │  (Qdrant)         │
   └───────────────────┘

   ┌──────────────────┐
   │  LLM Service     │
   │  (Ollama)        │
   └──────────────────┘
```

## Supported File Formats

- **PDF**: `.pdf` (via pdfplumber and PyPDF2)
- **Text**: `.txt` (UTF-8, Latin-1, CP1252)
- **Markdown**: `.md`
- **JSON**: `.json`
- **CSV**: `.csv`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ingest` | Upload and process documents |
| POST | `/api/v1/query` | Submit queries and get responses |
| GET | `/api/v1/documents` | List ingested documents |
| DELETE | `/api/v1/documents/{id}` | Remove a document |
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/agents/status` | Agent status |

## 🐛 Troubleshooting

### Port Already in Use
```bash
docker-compose down
docker-compose up -d
```

### Services Not Starting
```bash
docker-compose logs
docker-compose restart
```

### Streamlit Connection Error
```bash
# Verify API is running
curl http://localhost:8000/api/v1/health

# Check Streamlit logs in terminal
```

### No Documents Found
```bash
# Re-ingest sample data
bash scripts/ingest_sample_data.sh
```

### Slow Responses
- Check Docker resources: `docker stats`
- Verify Ollama is running: `docker-compose ps`
- Reduce `top_k` parameter in queries

## 📊 Test Results

✅ **All Tests Passed (5/5)**
- 🇬🇧 English: ✅ PASSED
- 🇪🇸 Spanish: ✅ PASSED
- 🇫🇷 French: ✅ PASSED
- 🇨🇳 Chinese: ✅ PASSED
- 🇸🇦 Arabic: ✅ PASSED

## 📁 Project Structure

```
multi_agentic_rag/
├── app/                    # Application code
├── scripts/                # Helper scripts
├── sample_data/            # Sample documents
├── streamlit_app.py        # Streamlit frontend
├── docker-compose.yml      # Docker configuration
├── requirements.txt        # Dependencies
├── INSTALLATION_GUIDE.md   # Installation steps
├── ARCHITECTURE.md         # System design
├── API_DOCS.md            # API documentation
└── README.md              # This file
```

## 📚 Documentation

- **INSTALLATION_GUIDE.md** - Step-by-step setup
- **ARCHITECTURE.md** - System design
- **API_DOCS.md** - API endpoints
- **INDEX.md** - File organization

## 🛑 Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📄 License

This project is provided as-is for educational and commercial use.

## 📞 Support

For detailed information:
- 📖 See **INSTALLATION_GUIDE.md** for setup
- 🏗️ See **ARCHITECTURE.md** for system design
- 📚 See **API_DOCS.md** for API details

---

**Version**: 1.0.0
**Status**: ✅ Production Ready
**Last Updated**: October 17, 2025

🎉 **Ready to use! Follow INSTALLATION_GUIDE.md to get started.**

