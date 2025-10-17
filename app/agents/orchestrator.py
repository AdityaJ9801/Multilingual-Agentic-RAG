"""Agent orchestrator for coordinating agent collaboration."""
from typing import Dict, Any, List
import time
from datetime import datetime
from app.agents.router import RouterAgent
from app.agents.retrieval import RetrievalAgent
from app.agents.synthesis import SynthesisAgent
from app.agents.validation import ValidationAgent
from app.models import AgentMessage
from app.utils.logger import get_logger
from app.config import get_settings

logger = get_logger(__name__)


class AgentOrchestrator:
    """Orchestrates collaboration between agents."""
    
    def __init__(self):
        """Initialize orchestrator with all agents."""
        self.router = RouterAgent()
        self.retrieval = RetrievalAgent()
        self.synthesis = SynthesisAgent()
        self.validation = ValidationAgent()
        
        self.agents = {
            "router": self.router,
            "retrieval": self.retrieval,
            "synthesis": self.synthesis,
            "validation": self.validation,
        }
        
        logger.info("Agent orchestrator initialized with 4 agents")
    
    async def process_query(
        self,
        query: str,
        language: str = "en",
        top_k: int = 5,
        include_validation: bool = True
    ) -> Dict[str, Any]:
        """
        Process a query through the agent pipeline.
        
        Args:
            query: User query
            language: Query language
            top_k: Number of documents to retrieve
            include_validation: Whether to include validation agent
            
        Returns:
            Final response with agent states
        """
        start_time = time.time()
        agent_states = {}
        
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # Step 1: Router Agent
            logger.debug("Step 1: Router Agent")
            router_message = AgentMessage(
                sender="user",
                receiver="router",
                message_type="query",
                content={
                    "query": query,
                    "language": language,
                    "top_k": top_k
                }
            )
            
            router_result = await self.router.process(router_message)
            agent_states["router"] = self.router.get_status()
            
            if not router_result.get("success"):
                logger.error("Router agent failed")
                return {
                    "success": False,
                    "error": router_result.get("error"),
                    "agent_states": agent_states
                }
            
            routing_decision = router_result.get("routing_decision", {})
            
            # Step 2: Retrieval Agent
            logger.debug("Step 2: Retrieval Agent")
            retrieval_message = AgentMessage(
                sender="router",
                receiver="retrieval",
                message_type="retrieve",
                content={
                    "query": query,
                    "language": language,
                    "top_k": top_k
                }
            )
            
            retrieval_result = await self.retrieval.process(retrieval_message)
            agent_states["retrieval"] = self.retrieval.get_status()
            
            if not retrieval_result.get("success"):
                logger.error("Retrieval agent failed")
                return {
                    "success": False,
                    "error": retrieval_result.get("error"),
                    "agent_states": agent_states
                }
            
            retrieval_data = retrieval_result.get("retrieval_result", {})
            documents = retrieval_data.get("documents", [])
            
            # Convert documents to dict format for synthesis
            documents_dict = [
                {
                    "id": doc.get("id"),
                    "content": doc.get("content"),
                    "metadata": doc.get("metadata", {})
                }
                for doc in documents
            ]
            
            # Step 3: Synthesis Agent
            logger.debug("Step 3: Synthesis Agent")
            synthesis_message = AgentMessage(
                sender="retrieval",
                receiver="synthesis",
                message_type="synthesize",
                content={
                    "query": query,
                    "language": language,
                    "documents": documents_dict
                }
            )
            
            synthesis_result = await self.synthesis.process(synthesis_message)
            agent_states["synthesis"] = self.synthesis.get_status()
            
            if not synthesis_result.get("success"):
                logger.error("Synthesis agent failed")
                return {
                    "success": False,
                    "error": synthesis_result.get("error"),
                    "agent_states": agent_states
                }
            
            synthesis_data = synthesis_result.get("synthesis_result", {})
            response = synthesis_data.get("response", "")
            sources = synthesis_data.get("sources", [])
            confidence = synthesis_data.get("confidence", 0.0)
            
            # Step 4: Validation Agent (optional)
            validation_data = {}
            if include_validation and routing_decision.get("requires_validation"):
                logger.debug("Step 4: Validation Agent")
                validation_message = AgentMessage(
                    sender="synthesis",
                    receiver="validation",
                    message_type="validate",
                    content={
                        "query": query,
                        "response": response,
                        "documents": documents_dict
                    }
                )
                
                validation_result = await self.validation.process(validation_message)
                agent_states["validation"] = self.validation.get_status()
                
                if validation_result.get("success"):
                    validation_data = validation_result.get("validation_result", {})
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            logger.info(f"Query processed successfully in {processing_time_ms:.2f}ms")
            
            return {
                "success": True,
                "response": response,
                "sources": sources,
                "confidence": confidence,
                "validation": validation_data,
                "processing_time_ms": processing_time_ms,
                "agent_states": agent_states,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Error in orchestrator: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent_states": agent_states
            }
    
    def get_agents_status(self) -> List[Dict[str, Any]]:
        """Get status of all agents."""
        return [agent.get_status() for agent in self.agents.values()]


# Global orchestrator instance
_orchestrator: AgentOrchestrator | None = None


def get_orchestrator() -> AgentOrchestrator:
    """Get or initialize the agent orchestrator."""
    global _orchestrator
    
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    
    return _orchestrator

