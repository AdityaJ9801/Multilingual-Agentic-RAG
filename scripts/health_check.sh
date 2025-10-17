#!/bin/bash

# Health check script for all services

echo "=========================================="
echo "RAG System Health Check"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service
check_service() {
    local name=$1
    local url=$2
    local port=$3
    
    echo -n "Checking $name... "
    
    if curl -s -f "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        return 1
    fi
}

# Function to check docker container
check_container() {
    local name=$1
    
    echo -n "Checking Docker container $name... "
    
    if docker ps --filter "name=$name" --filter "status=running" | grep -q "$name"; then
        echo -e "${GREEN}✓ Running${NC}"
        return 0
    else
        echo -e "${RED}✗ Not running${NC}"
        return 1
    fi
}

# Check Docker
echo "Docker Status:"
check_container "rag-ollama"
check_container "rag-qdrant"
check_container "rag-api"
echo ""

# Check Services
echo "Service Health:"
check_service "Ollama" "http://localhost:11434/api/tags" 11434
check_service "Qdrant" "http://localhost:6333/health" 6333
check_service "API" "http://localhost:8000/health" 8000
echo ""

# Check API endpoints
echo "API Endpoints:"
echo -n "GET /api/v1/documents... "
if curl -s -f "http://localhost:8000/api/v1/documents" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
fi

echo -n "GET /api/v1/agents/status... "
if curl -s -f "http://localhost:8000/api/v1/agents/status" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
fi
echo ""

# Check resource usage
echo "Resource Usage:"
echo "Docker containers:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
echo ""

# Check disk usage
echo "Disk Usage:"
df -h | grep -E "^/dev/|Filesystem"
echo ""

# Check volumes
echo "Docker Volumes:"
docker volume ls | grep rag
echo ""

echo "=========================================="
echo "Health Check Complete"
echo "=========================================="

