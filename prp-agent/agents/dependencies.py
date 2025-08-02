"""
Dependências para o agente PRP.

Este módulo define as dependências e configurações de contexto do agente.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from .settings import settings
import uuid
from datetime import datetime

@dataclass
class PRPAgentDependencies:
    """Dependências para o agente PRP."""
    
    # Database Configuration
    database_path: str = field(default_factory=lambda: settings.database_path)
    
    # Session Configuration
    session_id: str = field(default_factory=lambda: f"{settings.default_session_id}-{uuid.uuid4().hex[:8]}")
    user_id: Optional[str] = None
    
    # Analysis Configuration
    max_tokens_per_analysis: int = field(default_factory=lambda: settings.max_tokens_per_analysis)
    analysis_timeout: int = field(default_factory=lambda: settings.analysis_timeout)
    
    # Context Configuration
    project_context: Optional[Dict[str, Any]] = None
    conversation_history: Optional[list] = None
    
    # Performance Configuration
    enable_caching: bool = True
    cache_ttl: int = 3600  # 1 hora
    
    def __post_init__(self):
        """Inicialização pós-criação do dataclass."""
        if self.conversation_history is None:
            self.conversation_history = []
        
        if self.project_context is None:
            self.project_context = {
                "created_at": datetime.now().isoformat(),
                "agent_version": "1.0.0",
                "features": ["prp_analysis", "task_extraction", "database_integration"]
            }
    
    def add_conversation(self, message: str, response: str, metadata: Optional[Dict[str, Any]] = None):
        """Adicionar conversa ao histórico."""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "response": response,
            "metadata": metadata or {}
        }
        self.conversation_history.append(conversation)
    
    def get_recent_conversations(self, limit: int = 5) -> list:
        """Obter conversas recentes."""
        return self.conversation_history[-limit:] if self.conversation_history else []
    
    def update_project_context(self, key: str, value: Any):
        """Atualizar contexto do projeto."""
        self.project_context[key] = value
    
    def get_project_context(self, key: str, default: Any = None) -> Any:
        """Obter valor do contexto do projeto."""
        return self.project_context.get(key, default) if self.project_context else default 