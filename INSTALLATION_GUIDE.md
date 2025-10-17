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

## 📋 Prerequisites

### System Requirements
- ✅ 8GB RAM minimum (16GB recommended)
- ✅ 20GB disk space
- ✅ Internet connection (for Docker images)

### Software Requirements
- ✅ Docker & Docker Compose (v20.10+)
- ✅ Python 3.9+
- ✅ Git (for cloning repository)

---

## 🖥️ Platform-Specific Installation

### 🪟 **Windows Installation**

#### Step 1: Install Docker Desktop
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Run the installer and follow the setup wizard
3. Enable WSL 2 (Windows Subsystem for Linux 2) when prompted
4. Restart your computer
5. Verify installation:
```bash
docker --version
docker-compose --version
```

#### Step 2: Install Python
1. Download Python 3.9+ from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
```bash
python --version
pip --version
```

#### Step 3: Install Git
1. Download Git from https://git-scm.com/download/win
2. Run the installer with default settings
3. Verify installation:
```bash
git --version
```

#### Step 4: Clone Project
```bash
# Open Command Prompt or PowerShell
git clone <repository-url>
cd multi_agentic_rag
```

#### Step 5: Start Services
```bash
# Start Docker services
docker-compose up -d

# Wait for services to initialize (60 seconds)
timeout /t 60
```

#### Step 6: Ingest Sample Data
```bash
# Run the ingestion script
python scripts/test_multilingual_python.py
```

#### Step 7: Install Streamlit
```bash
pip install -r streamlit_requirements.txt
```

#### Step 8: Launch Application
```bash
streamlit run streamlit_app.py
```

#### Step 9: Access Application
- 🎨 **Streamlit UI**: http://localhost:8501
- 📚 **API Docs**: http://localhost:8000/docs
- ✅ **Health Check**: http://localhost:8000/api/v1/health

---

### 🐧 **Linux Installation**

#### Step 1: Install Docker
```bash
# Update package manager
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io docker-compose

# Add current user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

#### Step 2: Install Python
```bash
# Install Python 3.9+
sudo apt-get install -y python3.9 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

#### Step 3: Install Git
```bash
sudo apt-get install -y git

# Verify installation
git --version
```

#### Step 4: Clone Project
```bash
git clone <repository-url>
cd multi_agentic_rag
```

#### Step 5: Start Services
```bash
# Start Docker services
docker-compose up -d

# Wait for services to initialize
sleep 60

# Verify services are running
docker-compose ps
```

#### Step 6: Ingest Sample Data
```bash
# Run the ingestion script
bash scripts/ingest_sample_data.sh
```

#### Step 7: Install Streamlit
```bash
pip3 install -r streamlit_requirements.txt
```

#### Step 8: Launch Application
```bash
streamlit run streamlit_app.py
```

#### Step 9: Access Application
- 🎨 **Streamlit UI**: http://localhost:8501
- 📚 **API Docs**: http://localhost:8000/docs
- ✅ **Health Check**: http://localhost:8000/api/v1/health

---

### 🍎 **macOS Installation**

#### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Docker Desktop
```bash
# Using Homebrew
brew install --cask docker

# Or download from https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
docker-compose --version
```

#### Step 3: Install Python
```bash
# Using Homebrew
brew install python@3.9

# Verify installation
python3 --version
pip3 --version
```

#### Step 4: Install Git
```bash
# Using Homebrew
brew install git

# Verify installation
git --version
```

#### Step 5: Clone Project
```bash
git clone <repository-url>
cd multi_agentic_rag
```

#### Step 6: Start Services
```bash
# Start Docker services
docker-compose up -d

# Wait for services to initialize
sleep 60

# Verify services are running
docker-compose ps
```

#### Step 7: Ingest Sample Data
```bash
# Run the ingestion script
bash scripts/ingest_sample_data.sh
```

#### Step 8: Install Streamlit
```bash
pip3 install -r streamlit_requirements.txt
```

#### Step 9: Launch Application
```bash
streamlit run streamlit_app.py
```

#### Step 10: Access Application
- 🎨 **Streamlit UI**: http://localhost:8501
- 📚 **API Docs**: http://localhost:8000/docs
- ✅ **Health Check**: http://localhost:8000/api/v1/health

---

## 🚀 Quick Start (5 Minutes)

### Universal Quick Start (All Platforms)

```bash
# 1. Clone Project
git clone <repository-url>
cd multi_agentic_rag

# 2. Start Services
docker-compose up -d
sleep 60  # Wait for services to initialize

# 3. Ingest Sample Data
bash scripts/ingest_sample_data.sh

# 4. Install Streamlit
pip install -r streamlit_requirements.txt

# 5. Launch Application
streamlit run streamlit_app.py

# 6. Access Application
# Open http://localhost:8501 in your browser
```

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

### Common Issues (All Platforms)

#### Port Already in Use
```bash
docker-compose down
docker-compose up -d
```

#### Services Not Starting
```bash
docker-compose logs
docker-compose restart
```

#### Streamlit Connection Error
```bash
# Verify API is running
curl http://localhost:8000/api/v1/health

# Check Streamlit logs in terminal
```

#### No Documents Found
```bash
# Re-ingest sample data
bash scripts/ingest_sample_data.sh
```

#### Slow Responses
- Check Docker resources: `docker stats`
- Verify Ollama is running: `docker-compose ps`
- Reduce `top_k` parameter in queries

---

### 🪟 Windows-Specific Issues

#### Docker Not Starting
- Ensure WSL 2 is enabled
- Check if Hyper-V is enabled in Windows
- Restart Docker Desktop
- Restart your computer

#### PowerShell Execution Policy Error
```powershell
# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Command Not Found (Python/Git)
- Ensure Python and Git are added to PATH
- Restart Command Prompt or PowerShell after installation
- Verify: `python --version` and `git --version`

#### WSL 2 Not Installed
```bash
# Install WSL 2
wsl --install

# Restart your computer
# Then run Docker Desktop again
```

---

### 🐧 Linux-Specific Issues

#### Permission Denied Error
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker

# Verify
docker ps
```

#### Docker Daemon Not Running
```bash
# Start Docker service
sudo systemctl start docker

# Enable on boot
sudo systemctl enable docker

# Verify
docker ps
```

#### Python3 Not Found
```bash
# Install Python 3.9+
sudo apt-get install -y python3.9 python3-pip

# Create alias (optional)
alias python=python3
alias pip=pip3
```

#### Port Already in Use (Linux)
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or use docker-compose
docker-compose down
docker-compose up -d
```

---

### 🍎 macOS-Specific Issues

#### Docker Not Starting
- Ensure Docker Desktop is installed from App Store or official website
- Check System Preferences → Security & Privacy
- Restart Docker Desktop
- Restart your Mac

#### Homebrew Not Found
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH (if needed)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### Python Command Not Found
```bash
# Use python3 instead of python
python3 --version

# Create alias (optional)
echo "alias python=python3" >> ~/.zprofile
source ~/.zprofile
```

#### Port Already in Use (macOS)
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or use docker-compose
docker-compose down
docker-compose up -d
```

#### M1/M2 Mac Issues
- Docker Desktop for Apple Silicon is required
- Download from: https://www.docker.com/products/docker-desktop
- Most images are compatible, but some may need arm64 versions

## ✅ Verification Checklist

After installation, verify everything is working:

```bash
# 1. Check Docker services
docker-compose ps

# Expected output: 3 services running (api, qdrant, ollama)

# 2. Test API health
curl http://localhost:8000/api/v1/health

# Expected output: {"status":"healthy","version":"1.0.0"}

# 3. Check Streamlit is accessible
# Open http://localhost:8501 in browser

# 4. Test a query
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What is AI?","language":"en","top_k":5}'
```

---

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


