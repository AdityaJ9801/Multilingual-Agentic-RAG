"""Base agent class."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from app.models import AgentState, AgentMessage
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, name: str):
        """
        Initialize agent.
        
        Args:
            name: Agent name
        """
        self.name = name
        self.state = AgentState(
            agent_name=name,
            status="idle"
        )
        self.processed_queries = 0
        self.error_count = 0
    
    @abstractmethod
    async def process(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Process a message.
        
        Args:
            message: Input message
            
        Returns:
            Processing result
        """
        pass
    
    def update_status(self, status: str, current_task: Optional[str] = None) -> None:
        """Update agent status."""
        self.state.status = status
        self.state.current_task = current_task
        self.state.last_update = datetime.utcnow()
        logger.debug(f"Agent {self.name} status: {status}")
    
    def increment_processed_queries(self) -> None:
        """Increment processed queries counter."""
        self.processed_queries += 1
        self.state.metrics["processed_queries"] = self.processed_queries
    
    def increment_error_count(self) -> None:
        """Increment error counter."""
        self.error_count += 1
        self.state.metrics["error_count"] = self.error_count
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_name": self.name,
            "status": self.state.status,
            "current_task": self.state.current_task,
            "last_update": self.state.last_update.isoformat(),
            "processed_queries": self.processed_queries,
            "error_count": self.error_count,
        }

