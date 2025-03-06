"""Common type definitions for pymeepo.

This module defines common types used across the pymeepo package,
including type aliases, enums, and protocol classes.
"""

from enum import Enum
from typing import Any, Protocol, TypeAlias

from pydantic import BaseModel, Field


# Role definitions
class Role(str, Enum):
    """Enumeration of possible message roles."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    FUNCTION = "function"


# Function calling related types
class FunctionParameter(BaseModel):
    """Definition of a parameter for a function."""

    param_name: str = Field(..., description="The name of the parameter")
    description: str | None = Field(
        None, description="Description of the parameter"
    )
    param_type: str = Field(..., description="The type of the parameter")
    required: bool = Field(
        True, description="Whether the parameter is required"
    )
    default: Any | None = Field(
        None, description="Default value for the parameter"
    )


class FunctionDefinition(BaseModel):
    """Definition of a function that can be called by an agent."""

    name: str = Field(..., description="The name of the function")
    description: str = Field(
        ..., description="Description of what the function does"
    )
    parameters: dict[str, FunctionParameter] = Field(
        {}, description="Parameters for the function"
    )


class FunctionCall(BaseModel):
    """Representation of a function call in a message."""

    name: str = Field(..., description="The name of the function to call")
    arguments: dict[str, Any] = Field(
        {}, description="Arguments to pass to the function"
    )
    result: Any | None = Field(
        None, description="Result of the function call, if available"
    )


# Content type definitions
ContentItem: TypeAlias = str | dict[str, Any]
Content: TypeAlias = str | list[ContentItem]


# Agent-related types
class AgentType(str, Enum):
    """Enumeration of supported agent types."""

    ASSISTANT = "assistant"
    CODE_EXECUTOR = "code_executor"
    USER_PROXY = "user_proxy"
    SOCIETY_OF_MIND = "society_of_mind"
    CUSTOM = "custom"


class AgentConfig(BaseModel):
    """Base configuration for agents."""

    name: str = Field(..., description="The name of the agent")
    agent_type: AgentType = Field(
        AgentType.CUSTOM, description="The type of the agent"
    )
    description: str = Field(
        "", description="Description of the agent's capabilities"
    )


# Protocol classes
class AgentProtocol(Protocol):
    """Protocol defining the required interface for agents."""

    name: str
    description: str

    async def generate_response(self, message: Any) -> Any:
        """Generate a response to a message."""


# Other common types
LLMProvider: TypeAlias = str
MessageId: TypeAlias = str
AgentId: TypeAlias = str
