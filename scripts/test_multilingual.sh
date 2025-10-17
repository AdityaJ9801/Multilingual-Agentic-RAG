#!/bin/bash

# Test script for multilingual queries

API_URL="http://localhost:8000/api/v1"
API_KEY="your-api-key-change-in-production"

echo "=========================================="
echo "Multilingual Query Test"
echo "=========================================="
echo ""

# Function to test query
test_query() {
    local language=$1
    local query=$2
    local lang_name=$3

    echo "Testing $lang_name query..."
    echo "Query: $query"
    echo ""

    # Create JSON payload with proper escaping
    local json_payload=$(cat <<EOF
{
    "query": "$query",
    "language": "$language",
    "top_k": 3,
    "include_sources": true
}
EOF
)

    response=$(curl -s -X POST "$API_URL/query" \
        -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        -d "$json_payload")

    echo "Response:"
    echo "$response" | python -m json.tool 2>/dev/null || echo "$response"
    echo ""
    echo "---"
    echo ""
}

# Check if API is running
echo "Checking API health..."
if ! curl -s "$API_URL/health" > /dev/null; then
    echo "❌ API is not running. Please start the services first."
    echo "Run: docker-compose up -d"
    exit 1
fi
echo "✓ API is running"
echo ""

# Test queries in different languages
test_query "en" "What is artificial intelligence?" "English"
test_query "es" "¿Qué es la inteligencia artificial?" "Spanish"
test_query "fr" "Qu'est-ce que l'intelligence artificielle?" "French"
test_query "zh" "什么是人工智能?" "Chinese"
test_query "ar" "ما هو الذكاء الاصطناعي؟" "Arabic"

echo "=========================================="
echo "Test Complete!"
echo "=========================================="

