#!/bin/bash

# Setup script for Multilingual Agentic RAG System

set -e

echo "=========================================="
echo "Multilingual Agentic RAG - Setup Script"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p data
echo "✓ Directories created"
echo ""

# Start services
echo "Starting services..."
docker-compose up -d

echo "✓ Services started"
echo ""

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check Ollama
echo "Checking Ollama..."
if docker exec rag-ollama curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✓ Ollama is ready"
else
    echo "⚠ Ollama is not responding yet. It may still be starting."
fi
echo ""

# Check Qdrant
echo "Checking Qdrant..."
if docker exec rag-qdrant curl -s http://localhost:6333/health > /dev/null; then
    echo "✓ Qdrant is ready"
else
    echo "⚠ Qdrant is not responding yet. It may still be starting."
fi
echo ""

# Check API
echo "Checking API..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✓ API is ready"
else
    echo "⚠ API is not responding yet. It may still be starting."
fi
echo ""

# Pull default model
echo "Pulling default Ollama model (mistral)..."
echo "This may take a few minutes..."
docker exec rag-ollama ollama pull mistral || echo "⚠ Model pull failed. You can pull it manually later."
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. View API documentation: http://localhost:8000/docs"
echo "2. Check health: curl http://localhost:8000/health"
echo "3. Upload documents: curl -X POST http://localhost:8000/api/v1/ingest -F 'file=@document.pdf'"
echo "4. Query: curl -X POST http://localhost:8000/api/v1/query -H 'Content-Type: application/json' -d '{\"query\": \"Your question here\"}'"
echo ""
echo "View logs:"
echo "  docker-compose logs -f api"
echo "  docker-compose logs -f ollama"
echo "  docker-compose logs -f qdrant"
echo ""

