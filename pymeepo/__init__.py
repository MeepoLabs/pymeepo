"""pymeepo: A universal SDK for building and using AI agents.

pymeepo provides a unified interface for working with AI agents from various
frameworks, allowing seamless integration and interoperability.
"""

__version__ = "0.1.0"

from .core.agent import AsyncMeepoAgent, MeepoAgent
from .core.message import Conversation, Message
from .core.types import AgentConfig, AgentType, Role

__all__ = [
    "AsyncMeepoAgent",
    "MeepoAgent",
    "Conversation",
    "Message",
    "AgentType",
    "AgentConfig",
    "Role",
    "__version__",
]
