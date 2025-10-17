"""Synthesis agent for response generation."""
from typing import Dict, Any, List
import time
from app.agents.base import BaseAgent
from app.models import AgentMessage, SynthesisResult
from app.utils.logger import get_logger
from app.services.llm import generate_text

logger = get_logger(__name__)


class SynthesisAgent(BaseAgent):
    """Synthesizes responses from retrieved documents."""
    
    def __init__(self):
        """Initialize synthesis agent."""
        super().__init__("synthesis")
    
    async def process(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Generate a response based on retrieved documents.
        
        Args:
            message: Input message containing query and documents
            
        Returns:
            Synthesis result
        """
        self.update_status("processing", "synthesizing_response")
        start_time = time.time()
        
        try:
            query = message.content.get("query", "")
            language = message.content.get("language", "en")
            documents = message.content.get("documents", [])
            
            logger.info(f"Synthesizing response for query: {query[:100]}...")
            
            # Build context from documents
            context = self._build_context(documents)
            
            # Generate response
            prompt = self._build_prompt(query, context, language)
            response = generate_text(prompt)
            
            # Extract sources
            sources = self._extract_sources(documents)
            
            # Calculate confidence
            confidence = self._calculate_confidence(documents)
            
            synthesis_time_ms = (time.time() - start_time) * 1000
            
            synthesis_result = SynthesisResult(
                response=response,
                sources=sources,
                confidence=confidence,
                synthesis_time_ms=synthesis_time_ms
            )
            
            self.update_status("idle")
            self.increment_processed_queries()
            
            logger.info(f"Generated response in {synthesis_time_ms:.2f}ms")
            
            return {
                "synthesis_result": synthesis_result.model_dump(),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error in synthesis agent: {e}")
            self.increment_error_count()
            self.update_status("error")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """Build context from documents."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[Document {i}]\n{doc.get('content', '')}")
        return "\n\n".join(context_parts)
    
    def _build_prompt(self, query: str, context: str, language: str) -> str:
        """Build prompt for LLM."""
        language_names = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "zh": "Chinese",
            "ar": "Arabic"
        }
        lang_name = language_names.get(language, "English")
        
        prompt = f"""You are a helpful assistant. Answer the following question based on the provided context.
Answer in {lang_name}.

Context:
{context}

Question: {query}

Answer:"""
        return prompt
    
    def _extract_sources(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Extract source information from documents."""
        sources = []
        for doc in documents:
            metadata = doc.get("metadata", {})
            source = metadata.get("source", "Unknown")
            if source not in sources:
                sources.append(source)
        return sources
    
    def _calculate_confidence(self, documents: List[Dict[str, Any]]) -> float:
        """Calculate confidence based on retrieved documents."""
        if not documents:
            return 0.0
        
        # Simple confidence calculation based on number of documents
        # In production, this could be more sophisticated
        confidence = min(len(documents) / 5.0, 1.0)
        return confidence

