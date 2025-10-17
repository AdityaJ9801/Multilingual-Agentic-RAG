"""Integration tests for the RAG system."""
import pytest
import asyncio
from app.agents.orchestrator import AgentOrchestrator
from app.utils.language import detect_language, is_language_supported
from app.utils.embeddings import generate_embedding


class TestLanguageDetection:
    """Test language detection functionality."""
    
    def test_english_detection(self):
        """Test English language detection."""
        text = "What is machine learning?"
        lang, confidence = detect_language(text)
        assert lang == "en"
        assert confidence > 0.5
    
    def test_spanish_detection(self):
        """Test Spanish language detection."""
        text = "¿Qué es el aprendizaje automático?"
        lang, confidence = detect_language(text)
        assert lang == "es"
        assert confidence > 0.5
    
    def test_french_detection(self):
        """Test French language detection."""
        text = "Qu'est-ce que l'apprentissage automatique?"
        lang, confidence = detect_language(text)
        assert lang == "fr"
        assert confidence > 0.5
    
    def test_chinese_detection(self):
        """Test Chinese language detection."""
        text = "什么是机器学习?"
        lang, confidence = detect_language(text)
        assert lang == "zh"
        assert confidence > 0.5
    
    def test_arabic_detection(self):
        """Test Arabic language detection."""
        text = "ما هو التعلم الآلي؟"
        lang, confidence = detect_language(text)
        assert lang == "ar"
        assert confidence > 0.5
    
    def test_language_support(self):
        """Test language support checking."""
        assert is_language_supported("en")
        assert is_language_supported("es")
        assert is_language_supported("fr")
        assert is_language_supported("zh")
        assert is_language_supported("ar")
        assert not is_language_supported("xx")


class TestEmbeddings:
    """Test embedding generation."""
    
    def test_embedding_generation(self):
        """Test single embedding generation."""
        text = "Machine learning is a subset of artificial intelligence"
        embedding = generate_embedding(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) == 384  # multilingual-e5-large dimension
        assert all(isinstance(x, float) for x in embedding)
    
    def test_embedding_similarity(self):
        """Test that similar texts have similar embeddings."""
        text1 = "Machine learning is a subset of artificial intelligence"
        text2 = "Machine learning is part of AI"
        
        emb1 = generate_embedding(text1)
        emb2 = generate_embedding(text2)
        
        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(emb1, emb2))
        norm1 = sum(a ** 2 for a in emb1) ** 0.5
        norm2 = sum(b ** 2 for b in emb2) ** 0.5
        similarity = dot_product / (norm1 * norm2)
        
        # Similar texts should have high similarity
        assert similarity > 0.7


class TestAgentOrchestrator:
    """Test agent orchestrator."""
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = AgentOrchestrator()
        
        assert orchestrator.router is not None
        assert orchestrator.retrieval is not None
        assert orchestrator.synthesis is not None
        assert orchestrator.validation is not None
    
    @pytest.mark.asyncio
    async def test_agent_status(self):
        """Test getting agent status."""
        orchestrator = AgentOrchestrator()
        status = orchestrator.get_agents_status()
        
        assert len(status) == 4
        assert all("agent_name" in s for s in status)
        assert all("status" in s for s in status)


class TestLanguageConsistency:
    """Test language consistency across the system."""
    
    def test_multilingual_queries(self):
        """Test that queries in different languages are detected correctly."""
        queries = {
            "en": "What is artificial intelligence?",
            "es": "¿Qué es la inteligencia artificial?",
            "fr": "Qu'est-ce que l'intelligence artificielle?",
            "zh": "什么是人工智能?",
            "ar": "ما هو الذكاء الاصطناعي؟"
        }
        
        for expected_lang, query in queries.items():
            detected_lang, confidence = detect_language(query)
            assert detected_lang == expected_lang, \
                f"Expected {expected_lang}, got {detected_lang} for query: {query}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

