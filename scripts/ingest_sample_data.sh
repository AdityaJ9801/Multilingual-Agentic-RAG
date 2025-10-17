#!/bin/bash

# Script to ingest sample data

API_URL="http://localhost:8000/api/v1"
API_KEY="your-api-key-change-in-production"
SAMPLE_DATA_DIR="sample_data"

echo "=========================================="
echo "Sample Data Ingestion"
echo "=========================================="
echo ""

# Check if API is running
echo "Checking API health..."
if ! curl -s "$API_URL/health" > /dev/null; then
    echo "❌ API is not running. Please start the services first."
    echo "Run: docker-compose up -d"
    exit 1
fi
echo "✓ API is running"
echo ""

# Create sample data directory if it doesn't exist
if [ ! -d "$SAMPLE_DATA_DIR" ]; then
    echo "Creating sample data directory..."
    mkdir -p "$SAMPLE_DATA_DIR"
    
    # Create sample text files in different languages
    cat > "$SAMPLE_DATA_DIR/machine_learning_en.txt" << 'EOF'
Machine Learning

Machine learning is a subset of artificial intelligence (AI) that focuses on the development of algorithms and statistical models that enable computers to learn and improve from experience without being explicitly programmed.

Key Concepts:
1. Supervised Learning: Learning from labeled data
2. Unsupervised Learning: Finding patterns in unlabeled data
3. Reinforcement Learning: Learning through interaction and rewards

Applications:
- Image recognition
- Natural language processing
- Recommendation systems
- Autonomous vehicles
- Medical diagnosis

Machine learning has revolutionized many industries and continues to be a rapidly growing field.
EOF

    cat > "$SAMPLE_DATA_DIR/machine_learning_es.txt" << 'EOF'
Aprendizaje Automático

El aprendizaje automático es un subconjunto de la inteligencia artificial (IA) que se enfoca en el desarrollo de algoritmos y modelos estadísticos que permiten a las computadoras aprender y mejorar a partir de la experiencia sin ser programadas explícitamente.

Conceptos Clave:
1. Aprendizaje Supervisado: Aprendizaje a partir de datos etiquetados
2. Aprendizaje No Supervisado: Encontrar patrones en datos sin etiquetar
3. Aprendizaje por Refuerzo: Aprendizaje a través de interacción y recompensas

Aplicaciones:
- Reconocimiento de imágenes
- Procesamiento del lenguaje natural
- Sistemas de recomendación
- Vehículos autónomos
- Diagnóstico médico
EOF

    cat > "$SAMPLE_DATA_DIR/machine_learning_fr.txt" << 'EOF'
Apprentissage Automatique

L'apprentissage automatique est un sous-ensemble de l'intelligence artificielle (IA) qui se concentre sur le développement d'algorithmes et de modèles statistiques qui permettent aux ordinateurs d'apprendre et de s'améliorer à partir de l'expérience sans être explicitement programmés.

Concepts Clés:
1. Apprentissage Supervisé: Apprentissage à partir de données étiquetées
2. Apprentissage Non Supervisé: Trouver des modèles dans les données non étiquetées
3. Apprentissage par Renforcement: Apprentissage par interaction et récompenses

Applications:
- Reconnaissance d'images
- Traitement du langage naturel
- Systèmes de recommandation
- Véhicules autonomes
- Diagnostic médical
EOF

    echo "✓ Sample data files created"
else
    echo "✓ Sample data directory already exists"
fi
echo ""

# Ingest sample files
echo "Ingesting sample files..."
for file in "$SAMPLE_DATA_DIR"/*.txt; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "Ingesting: $filename"
        
        response=$(curl -s -X POST "$API_URL/ingest" \
            -H "X-API-Key: $API_KEY" \
            -F "file=@$file")
        
        echo "$response" | jq '.' 2>/dev/null || echo "$response"
        echo ""
    fi
done

echo "=========================================="
echo "Sample Data Ingestion Complete!"
echo "=========================================="
echo ""
echo "You can now test queries with the ingested data:"
echo "  ./scripts/test_multilingual.sh"

