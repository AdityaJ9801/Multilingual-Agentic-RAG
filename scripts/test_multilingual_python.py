#!/usr/bin/env python3
"""Multilingual test script for the RAG system."""

import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:8000/api/v1"
API_KEY = "your-api-key-change-in-production"

# Test queries in different languages
test_queries = [
    {
        "language": "en",
        "query": "What is artificial intelligence?",
        "lang_name": "English"
    },
    {
        "language": "es",
        "query": "¿Qué es la inteligencia artificial?",
        "lang_name": "Spanish"
    },
    {
        "language": "fr",
        "query": "Qu'est-ce que l'intelligence artificielle?",
        "lang_name": "French"
    },
    {
        "language": "zh",
        "query": "什么是人工智能?",
        "lang_name": "Chinese"
    },
    {
        "language": "ar",
        "query": "ما هو الذكاء الاصطناعي؟",
        "lang_name": "Arabic"
    }
]

def test_query(language, query, lang_name):
    """Test a query in a specific language."""
    print(f"\nTesting {lang_name} query...")
    print(f"Query: {query}")
    print("-" * 80)
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/query",
            headers={
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "query": query,
                "language": language,
                "top_k": 3,
                "include_sources": True
            },
            timeout=300
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: Success")
            print(f"Language Detected: {data.get('language', 'N/A')}")
            print(f"Response: {data.get('response', 'N/A')[:200]}...")
            print(f"Confidence: {data.get('confidence', 0.0):.2f}")
            print(f"Processing Time: {data.get('processing_time_ms', 0):.2f}ms")
            print(f"Total Elapsed Time: {elapsed_time:.2f}s")
            
            # Check if response is in the same language
            detected_lang = data.get('language', '')
            if detected_lang == language:
                print(f"✅ Language Match: Response is in {lang_name}")
            else:
                print(f"⚠️ Language Mismatch: Expected {language}, got {detected_lang}")
            
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("Multilingual Query Test")
    print("=" * 80)
    
    # Check API health
    print("\nChecking API health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ API is running")
        else:
            print(f"❌ API returned status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ API is not running: {str(e)}")
        return
    
    # Run tests
    results = []
    for test in test_queries:
        result = test_query(
            test["language"],
            test["query"],
            test["lang_name"]
        )
        results.append({
            "language": test["lang_name"],
            "success": result
        })
    
    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status}: {result['language']}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")

if __name__ == "__main__":
    main()

