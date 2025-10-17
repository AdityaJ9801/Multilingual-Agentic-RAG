# ⚡ Quick Setup Guide - 5 Minutes

## 🎯 Goal
Get the Multilingual Agentic RAG System running in 5 minutes.

---

## ✅ Prerequisites

Before starting, ensure you have:
- ✅ Docker Desktop installed (https://www.docker.com/products/docker-desktop)
- ✅ Python 3.9+ installed (https://www.python.org/)
- ✅ 8GB RAM available
- ✅ 20GB disk space available

**Check Installation:**
```bash
docker --version
python --version
```

---

## 🚀 Step-by-Step Setup

### Step 1: Extract Project (1 minute)

**Windows:**
```bash
# Right-click ZIP file → Extract All
# Or use command:
tar -xf multilingual_rag.zip
cd multi_agentic_rag
```

**macOS/Linux:**
```bash
unzip multilingual_rag.zip
cd multi_agentic_rag
```

---

### Step 2: Start Docker Services (2 minutes)

```bash
# Start all services
docker-compose up -d

# Wait for services to initialize
sleep 60

# Verify services are running
docker-compose ps
```

**Expected Output:**
```
NAME                COMMAND                  STATUS
qdrant              "/qdrant/qdrant ..."     Up
ollama              "/bin/sh -c 'ollama..."  Up
api                 "python -m uvicorn..."   Up
```

---

### Step 3: Ingest Sample Data (1 minute)

```bash
# Load sample documents into the system
bash scripts/ingest_sample_data.sh

# Or on Windows:
python scripts/test_multilingual_python.py
```

**Expected Output:**
```
✅ Documents ingested successfully
✅ Embeddings created
✅ Vector database updated
```

---

### Step 4: Install Streamlit (1 minute)

```bash
# Install Streamlit dependencies
pip install -r streamlit_requirements.txt
```

---

### Step 5: Launch Application (1 minute)

```bash
# Start Streamlit app
streamlit run streamlit_app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

## 🎨 Access Application

### Open in Browser
```
http://localhost:8501
```

### What You'll See
- **Query Tab**: Submit queries in any language
- **Upload Tab**: Upload your own documents
- **Documents Tab**: Manage uploaded files
- **Analytics Tab**: Monitor system

---

## 🧪 Quick Test

### Test 1: Via Streamlit (Easiest)
1. Open http://localhost:8501
2. Go to **Query** tab
3. Type: "What is artificial intelligence?"
4. Click **Submit**
5. ✅ You should see a response!

### Test 2: Via API (Advanced)
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is AI?",
    "language": "en",
    "top_k": 5,
    "include_sources": true
  }'
```

### Test 3: Health Check
```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response:**
```json
{"status":"healthy","version":"1.0.0"}
```

---

## 🌍 Try Different Languages

### English
```
Query: "What is machine learning?"
```

### Spanish
```
Query: "¿Qué es el aprendizaje automático?"
```

### French
```
Query: "Qu'est-ce que l'apprentissage automatique?"
```

### Chinese
```
Query: "什么是机器学习?"
```

### Arabic
```
Query: "ما هو التعلم الآلي?"
```

---

## 🛑 Stopping the System

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

---

## 🐛 Troubleshooting

### Issue: Port Already in Use
```bash
docker-compose down
docker-compose up -d
```

### Issue: Services Not Starting
```bash
docker-compose logs
docker-compose restart
```

### Issue: Streamlit Won't Connect
```bash
# Check if API is running
curl http://localhost:8000/api/v1/health

# Restart Streamlit
# Press Ctrl+C in terminal
streamlit run streamlit_app.py
```

### Issue: No Documents Found
```bash
# Re-ingest sample data
bash scripts/ingest_sample_data.sh
```

---

## 📚 Next Steps

### Learn More
- Read **README.md** for overview
- Read **INSTALLATION_GUIDE.md** for detailed setup
- Read **ARCHITECTURE.md** for system design
- Read **API_DOCS.md** for API details

### Upload Your Own Documents
1. Open http://localhost:8501
2. Go to **Upload** tab
3. Select your document
4. Click **Upload**
5. Query your documents!

### Customize Configuration
1. Edit `.env` file
2. Restart services: `docker-compose restart`

---

## ✅ Verification Checklist

- [ ] Docker installed and running
- [ ] Python 3.9+ installed
- [ ] Project extracted
- [ ] Services started (`docker-compose ps` shows 3 services)
- [ ] Sample data ingested
- [ ] Streamlit installed
- [ ] Application accessible at http://localhost:8501
- [ ] Can submit a query
- [ ] Received a response

---

## 📊 System Status

After setup, you should have:
- ✅ FastAPI backend running on port 8000
- ✅ Streamlit frontend running on port 8501
- ✅ Qdrant vector database on port 6333
- ✅ Ollama LLM service on port 11434
- ✅ Sample documents loaded
- ✅ Ready to query in 5 languages

---

## 🎉 You're Done!

The system is now running and ready to use!

### What You Can Do Now
1. ✅ Query documents in 5 languages
2. ✅ Upload your own documents
3. ✅ View system analytics
4. ✅ Use the REST API
5. ✅ Explore the architecture

---

## 📞 Need Help?

1. Check **INSTALLATION_GUIDE.md** for detailed steps
2. Check **ARCHITECTURE.md** for system design
3. Check **API_DOCS.md** for API details
4. View logs: `docker-compose logs`
5. Check services: `docker-compose ps`

---

**⏱️ Total Setup Time: ~5 minutes**

**🎉 Ready to use the Multilingual Agentic RAG System!**

