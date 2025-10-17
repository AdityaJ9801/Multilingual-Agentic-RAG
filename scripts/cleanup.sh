#!/bin/bash

# Cleanup script for the RAG system

echo "=========================================="
echo "RAG System Cleanup"
echo "=========================================="
echo ""

# Ask for confirmation
read -p "This will stop and remove all containers. Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 1
fi

echo ""
echo "Stopping services..."
docker-compose down

echo "Removing volumes..."
read -p "Remove all data volumes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker volume rm rag-ollama rag-qdrant 2>/dev/null || true
    echo "Volumes removed"
fi

echo "Removing images..."
read -p "Remove Docker images? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker rmi rag-api:latest 2>/dev/null || true
    echo "Images removed"
fi

echo ""
echo "=========================================="
echo "Cleanup Complete"
echo "=========================================="

