"""Message classes and utilities for pymeepo.

This module defines message classes and utilities for agent communication.
"""

import uuid
from datetime import datetime
from typing import Any, cast

from pydantic import BaseModel, Field, field_validator

from .types import Content, FunctionCall, Role


class Message(BaseModel):
    """Base message class for agent communication."""

    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: Role
    content: Content
    name: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    function_call: FunctionCall | None = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: Any) -> Role:
        """Validate that the role is valid."""
        if isinstance(v, str):
            try:
                return Role(v)
            except ValueError as exc:
                raise ValueError(f"Invalid role: {v}") from exc
        # Cast to Role to satisfy mypy
        # We know v is already a Role at this point
        return cast(Role, v)

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary format compatible with LLMs."""
        result: dict[str, Any] = {
            "role": self.role.value,
            "content": self.content,
        }

        if self.name:
            result["name"] = self.name

        if self.function_call:
            # Convert FunctionCall to dict and add to result
            result["function_call"] = self.function_call.model_dump()

        return result

    @classmethod
    def system(cls, content: str, name: str | None = None) -> "Message":
        """Create a system message."""
        return cls(role=Role.SYSTEM, content=content, name=name)

    @classmethod
    def user(cls, content: str | list, name: str | None = None) -> "Message":
        """Create a user message."""
        return cls(role=Role.USER, content=content, name=name)

    @classmethod
    def assistant(
        cls,
        content: str | list,
        name: str | None = None,
        function_call: FunctionCall | None = None,
    ) -> "Message":
        """Create an assistant message."""
        return cls(
            role=Role.ASSISTANT,
            content=content,
            name=name,
            function_call=function_call,
        )

    @classmethod
    def tool(
        cls,
        content: str,
        name: str | None = None,
    ) -> "Message":
        """Create a tool message."""
        return cls(role=Role.TOOL, content=content, name=name)

    @classmethod
    def function(
        cls,
        content: str,
        name: str,
    ) -> "Message":
        """Create a function message."""
        return cls(role=Role.FUNCTION, content=content, name=name)


class Conversation(BaseModel):
    """A conversation between agents, containing a list of messages."""

    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: list[Message] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)

    def add_system_message(self, content: str, name: str | None = None) -> None:
        """Add a system message to the conversation."""
        self.add_message(Message.system(content, name))

    def add_user_message(
        self, content: str | list, name: str | None = None
    ) -> None:
        """Add a user message to the conversation."""
        self.add_message(Message.user(content, name))

    def add_assistant_message(
        self,
        content: str | list,
        name: str | None = None,
        function_call: FunctionCall | None = None,
    ) -> None:
        """Add an assistant message to the conversation."""
        self.add_message(Message.assistant(content, name, function_call))

    def add_tool_message(self, content: str, name: str | None = None) -> None:
        """Add a tool message to the conversation."""
        self.add_message(Message.tool(content, name))

    def add_function_message(self, content: str, name: str) -> None:
        """Add a function message to the conversation."""
        self.add_message(Message.function(content, name))

    def get_last_message(self) -> Message | None:
        """Get the last message in the conversation."""
        if not self.messages:
            return None
        return self.messages[-1]

    def clear(self) -> None:
        """Clear all messages in the conversation."""
        self.messages = []


# Adapter functions for message conversion
def from_autogen_message(message: Any) -> Message:
    """Convert an AutoGen message to a pymeepo Message."""
    # This will be implemented when we add AutoGen adapter
    return cast(Message, message)


def to_autogen_message(message: Message) -> Any:
    """Convert a pymeepo Message to an AutoGen message."""
    # This will be implemented when we add AutoGen adapter
    return message
