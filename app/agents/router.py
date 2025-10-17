"""Router agent for query routing."""
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models import AgentMessage, RoutingDecision
from app.utils.logger import get_logger
from app.utils.language import detect_language

logger = get_logger(__name__)


class RouterAgent(BaseAgent):
    """Routes queries to appropriate agents."""
    
    def __init__(self):
        """Initialize router agent."""
        super().__init__("router")
    
    async def process(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Route a query to appropriate agents.
        
        Args:
            message: Input message containing query
            
        Returns:
            Routing decision
        """
        self.update_status("processing", "routing_query")
        
        try:
            query = message.content.get("query", "")
            language = message.content.get("language")
            
            # Detect language if not provided
            if not language:
                language, _ = detect_language(query)
            
            # Determine query type and target agents
            query_type = self._determine_query_type(query)
            target_agents = self._determine_target_agents(query_type)
            
            routing_decision = RoutingDecision(
                query_type=query_type,
                target_agents=target_agents,
                priority=1,
                requires_retrieval=True,
                requires_validation=True,
                language=language
            )
            
            self.update_status("idle")
            self.increment_processed_queries()
            
            logger.info(f"Routed query to agents: {target_agents}")
            
            return {
                "routing_decision": routing_decision.model_dump(),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error in router agent: {e}")
            self.increment_error_count()
            self.update_status("error")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _determine_query_type(self, query: str) -> str:
        """Determine the type of query."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["what", "which", "who", "where"]):
            return "factual"
        elif any(word in query_lower for word in ["how", "explain", "describe"]):
            return "explanatory"
        elif any(word in query_lower for word in ["summarize", "summary", "brief"]):
            return "summarization"
        else:
            return "general"
    
    def _determine_target_agents(self, query_type: str) -> list:
        """Determine which agents should process the query."""
        base_agents = ["retrieval", "synthesis"]
        
        if query_type in ["factual", "explanatory"]:
            return base_agents + ["validation"]
        
        return base_agents

