"""Validation agent for fact-checking and citation verification."""
from typing import Dict, Any, List
import time
from app.agents.base import BaseAgent
from app.models import AgentMessage, ValidationResult
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ValidationAgent(BaseAgent):
    """Validates responses and verifies citations."""
    
    def __init__(self):
        """Initialize validation agent."""
        super().__init__("validation")
    
    async def process(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Validate response and verify citations.
        
        Args:
            message: Input message containing response and documents
            
        Returns:
            Validation result
        """
        self.update_status("processing", "validating_response")
        start_time = time.time()
        
        try:
            response = message.content.get("response", "")
            documents = message.content.get("documents", [])
            query = message.content.get("query", "")
            
            logger.info(f"Validating response for query: {query[:100]}...")
            
            # Perform validation checks
            issues = self._check_response_quality(response)
            citation_issues = self._verify_citations(response, documents)
            issues.extend(citation_issues)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(issues, response)
            
            # Calculate confidence
            is_valid = len(issues) == 0
            confidence = 1.0 - (len(issues) * 0.1)  # Reduce confidence for each issue
            confidence = max(0.0, min(1.0, confidence))
            
            validation_time_ms = (time.time() - start_time) * 1000
            
            validation_result = ValidationResult(
                is_valid=is_valid,
                confidence=confidence,
                issues=issues,
                suggestions=suggestions,
                validation_time_ms=validation_time_ms
            )
            
            self.update_status("idle")
            self.increment_processed_queries()
            
            logger.info(f"Validation completed in {validation_time_ms:.2f}ms. Valid: {is_valid}")
            
            return {
                "validation_result": validation_result.model_dump(),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error in validation agent: {e}")
            self.increment_error_count()
            self.update_status("error")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _check_response_quality(self, response: str) -> List[str]:
        """Check response quality."""
        issues = []
        
        # Check if response is too short
        if len(response.strip()) < 10:
            issues.append("Response is too short")
        
        # Check if response contains common error indicators
        error_indicators = ["i don't know", "unable to", "cannot determine"]
        if any(indicator in response.lower() for indicator in error_indicators):
            issues.append("Response indicates inability to answer")
        
        return issues
    
    def _verify_citations(self, response: str, documents: List[Dict[str, Any]]) -> List[str]:
        """Verify that response is supported by documents."""
        issues = []
        
        if not documents:
            issues.append("No source documents available for verification")
            return issues
        
        # Simple verification: check if response contains content from documents
        response_lower = response.lower()
        document_content = " ".join([doc.get("content", "").lower() for doc in documents])
        
        # Check for key terms overlap
        response_words = set(response_lower.split())
        document_words = set(document_content.split())
        
        overlap = len(response_words & document_words) / len(response_words) if response_words else 0
        
        if overlap < 0.3:
            issues.append("Response may not be fully supported by source documents")
        
        return issues
    
    def _generate_suggestions(self, issues: List[str], response: str) -> List[str]:
        """Generate suggestions for improvement."""
        suggestions = []
        
        if "too short" in str(issues):
            suggestions.append("Consider providing more detailed information")
        
        if "not fully supported" in str(issues):
            suggestions.append("Review source documents to ensure accuracy")
        
        if len(response) > 1000:
            suggestions.append("Consider summarizing the response for clarity")
        
        return suggestions

