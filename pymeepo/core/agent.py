"""Agent classes for pymeepo.

This module defines the core agent classes for pymeepo, including
AsyncMeepoAgent and MeepoAgent.
"""

import asyncio
import logging
from collections.abc import AsyncGenerator, Sequence
from typing import Any

from autogen_agentchat.agents._base_chat_agent import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import (
    AgentEvent,
    ChatMessage,
    ModelClientStreamingChunkEvent,
    TextMessage,
)
from autogen_agentchat.state import BaseState
from autogen_core import CancellationToken

from .message import Conversation, Message
from .types import AgentType

logger = logging.getLogger(__name__)


class AsyncMeepoAgent(BaseChatAgent):
    """Asynchronous agent class that extends AutoGen's BaseChatAgent.

    This class implements the AutoGen agent interface and serves as the
    foundation for pymeepo agents.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        agent_type: AgentType = AgentType.ASSISTANT,
        system_message: str | None = None,
        llm_config: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the AsyncMeepoAgent.

        Args:
            name: The name of the agent.
            description: A description of the agent's capabilities.
            agent_type: The type of agent.
            system_message: System message for the agent.
            llm_config: Configuration for the language model.
        """
        super().__init__(name=name, description=description)
        self.agent_type = agent_type
        self._system_message = system_message
        self._llm_config = llm_config or {}
        self._conversation = Conversation()

        # Initialize system message if provided
        if self._system_message:
            self._conversation.add_system_message(self._system_message)

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        """Return the types of messages that this agent can produce.

        Returns:
            A sequence of ChatMessage types.
        """
        return [TextMessage]

    async def on_messages(
        self,
        messages: Sequence[ChatMessage],
        cancellation_token: CancellationToken,
    ) -> Response:
        """Handle incoming messages and generate a response.

        Args:
            messages: The incoming messages to process.
            cancellation_token: Token for cancelling the operation.

        Returns:
            A Response object containing the agent's reply.
        """
        # Convert AutoGen messages to pymeepo messages
        pymeepo_messages = self._convert_autogen_messages(messages)

        # Add messages to conversation
        for message in pymeepo_messages:
            self._conversation.add_message(message)

        # Generate response
        response_content = await self._generate_response(
            self._conversation, cancellation_token
        )

        # Create response message with required source parameter
        response_message = TextMessage(
            content=response_content, source=self.name
        )

        return Response(chat_message=response_message)

    async def on_messages_stream(
        self,
        messages: Sequence[ChatMessage],
        cancellation_token: CancellationToken,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | Response, None]:
        """Handle incoming messages and stream the response.

        Args:
            messages: The incoming messages to process.
            cancellation_token: Token for cancelling the operation.

        Yields:
            Events, messages, and finally a Response.
        """
        # Convert AutoGen messages to pymeepo messages
        pymeepo_messages = self._convert_autogen_messages(messages)

        # Add messages to conversation
        for message in pymeepo_messages:
            self._conversation.add_message(message)

        # Stream response content
        response_content = ""

        # Yield streaming events
        async for chunk in self._generate_response_stream(
            self._conversation, cancellation_token
        ):
            response_content += chunk
            # Yield chunk events with required source parameter
            yield ModelClientStreamingChunkEvent(
                content=chunk, source=self.name
            )

        # Create final response message with required source parameter
        response_message = TextMessage(
            content=response_content, source=self.name
        )

        # Yield the final response
        yield Response(chat_message=response_message)

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        """Reset the agent to its initial state.

        Args:
            cancellation_token: Token for cancelling the operation.
        """
        self._conversation.clear()

        # Re-initialize system message if provided
        if self._system_message:
            self._conversation.add_system_message(self._system_message)

    async def on_save_state(self) -> BaseState:
        """Save the current state of the agent.

        Returns:
            The saved state.
        """
        # This is a placeholder - will be implemented in a future phase
        return BaseState()

    async def on_load_state(self, state: BaseState) -> None:
        """Load a saved state into the agent.

        Args:
            state: The state to load.
        """
        # This is a placeholder - will be implemented in a future phase
        del state

    async def _generate_response(
        self, conversation: Conversation, cancellation_token: CancellationToken
    ) -> str:
        """Generate a response based on the conversation.

        Args:
            conversation: The conversation to generate a response for.
            cancellation_token: Token for cancelling the operation.

        Returns:
            The generated response text.
        """
        # This is a placeholder that would be overridden by subclasses
        # or replaced with actual LLM calls in the future
        del conversation
        del cancellation_token
        return "This is a placeholder response from AsyncMeepoAgent."

    async def _generate_response_stream(
        self, conversation: Conversation, cancellation_token: CancellationToken
    ) -> AsyncGenerator[str, None]:
        """Stream a response based on the conversation.

        Args:
            conversation: The conversation to generate a response for.
            cancellation_token: Token for cancelling the operation.

        Yields:
            Chunks of the generated response.
        """
        # This is a placeholder stream generator
        chunks = [
            "This ",
            "is ",
            "a ",
            "placeholder ",
            "response ",
            "from ",
            "AsyncMeepoAgent.",
        ]

        for chunk in chunks:
            yield chunk
            await asyncio.sleep(0.1)  # Simulate streaming delay
        del conversation
        del cancellation_token

    def _convert_autogen_messages(
        self, messages: Sequence[ChatMessage]
    ) -> list[Message]:
        """Convert AutoGen messages to pymeepo messages.

        Args:
            messages: The AutoGen messages to convert.

        Returns:
            A list of converted pymeepo messages.
        """
        # This is a placeholder conversion - will be properly implemented
        # when we add the AutoGen adapter
        result = []
        for msg in messages:
            # AutoGen ChatMessage doesn't have a role attribute directly
            # We need to determine the role based on message type
            content = msg.content

            # This is a simplified approach - we'll enhance this in adapter
            if isinstance(msg, TextMessage):
                # For simplicity, treat all TextMessages as user messages
                # Will be refined in the adapter implementation
                result.append(Message.user(content))
            else:
                # Default to user for unknown message types
                result.append(Message.user(str(content)))

        return result

    @classmethod
    def create_assistant(
        cls,
        name: str,
        llm: str = "gpt-4",
        system_message: str | None = None,
        description: str = "A helpful AI assistant",
        **kwargs: Any,
    ) -> "AsyncMeepoAgent":
        """Create an assistant agent.

        Args:
            name: The name of the agent.
            llm: The language model to use.
            system_message: System message for the agent.
            description: A description of the agent's capabilities.
            **kwargs: Additional arguments to pass to the constructor.

        Returns:
            An AsyncMeepoAgent configured as an assistant.
        """
        llm_config = {"model": llm, **kwargs.pop("llm_config", {})}

        return cls(
            name=name,
            description=description,
            agent_type=AgentType.ASSISTANT,
            system_message=system_message or "You are a helpful AI assistant.",
            llm_config=llm_config,
            **kwargs,
        )

    @classmethod
    def create_code_executor(
        cls,
        name: str,
        llm: str = "gpt-4",
        system_message: str | None = None,
        description: str = "An agent that can execute code",
        **kwargs: Any,
    ) -> "AsyncMeepoAgent":
        """Create a code executor agent.

        Args:
            name: The name of the agent.
            llm: The language model to use.
            system_message: System message for the agent.
            description: A description of the agent's capabilities.
            **kwargs: Additional arguments to pass to the constructor.

        Returns:
            An AsyncMeepoAgent configured as a code executor.
        """
        llm_config = {"model": llm, **kwargs.pop("llm_config", {})}

        return cls(
            name=name,
            description=description,
            agent_type=AgentType.CODE_EXECUTOR,
            system_message=system_message
            or (
                "You are a code execution agent capable of running code and "
                "returning the results."
            ),
            llm_config=llm_config,
            **kwargs,
        )

    @classmethod
    def create_user_proxy(
        cls,
        name: str,
        description: str = "A user proxy agent",
        **kwargs: Any,
    ) -> "AsyncMeepoAgent":
        """Create a user proxy agent.

        Args:
            name: The name of the agent.
            description: A description of the agent's capabilities.
            **kwargs: Additional arguments to pass to the constructor.

        Returns:
            An AsyncMeepoAgent configured as a user proxy.
        """
        return cls(
            name=name,
            description=description,
            agent_type=AgentType.USER_PROXY,
            **kwargs,
        )

    @classmethod
    def from_agent(
        cls, agent: Any, name: str | None = None
    ) -> "AsyncMeepoAgent":
        """Create an AsyncMeepoAgent from another agent.

        Args:
            agent: The agent to wrap.
            name: Optional name for the new agent.

        Returns:
            An AsyncMeepoAgent wrapping the provided agent.
        """
        # This is a placeholder - will be implemented in a future phase
        # when we add adapters for other agent frameworks
        agent_name = (
            name
            if name is not None
            else str(getattr(agent, "name", "wrapped_agent"))
        )
        return cls(
            name=agent_name,
            description=getattr(agent, "description", ""),
        )


class MeepoAgent:
    """Synchronous wrapper around AsyncMeepoAgent.

    This class provides a synchronous interface to AsyncMeepoAgent, making it
    easier to use in non-async contexts.
    """

    def __init__(self, async_agent: AsyncMeepoAgent) -> None:
        """Initialize the MeepoAgent.

        Args:
            async_agent: The AsyncMeepoAgent to wrap.
        """
        self._async_agent = async_agent

    @property
    def name(self) -> str:
        """Get the name of the agent.

        Returns:
            The agent's name.
        """
        return str(self._async_agent.name)

    @property
    def description(self) -> str:
        """Get the description of the agent.

        Returns:
            The agent's description.
        """
        return str(self._async_agent.description)

    @property
    def agent_type(self) -> AgentType:
        """Get the type of the agent.

        Returns:
            The agent's type.
        """
        return self._async_agent.agent_type

    def generate_response(self, message: str | Message) -> str:
        """Generate a response to a message.

        Args:
            message: The message to respond to.

        Returns:
            The generated response text.
        """
        # Convert to Conversation if needed
        conversation = self._prepare_conversation(message)

        # Run the async method in a synchronous context
        loop = asyncio.get_event_loop()
        cancel_token = CancellationToken()

        # This is a simplified version - in a real implementation,
        # we would convert the message to an AutoGen message and pass
        # it to on_messages
        return loop.run_until_complete(
            self._async_agent._generate_response(conversation, cancel_token)
        )

    def reset(self) -> None:
        """Reset the agent to its initial state."""
        loop = asyncio.get_event_loop()
        cancel_token = CancellationToken()
        loop.run_until_complete(self._async_agent.on_reset(cancel_token))

    def _prepare_conversation(self, message: str | Message) -> Conversation:
        """Prepare a conversation from a message.

        Args:
            message: The message to prepare a conversation for.

        Returns:
            A conversation containing the message.
        """
        conversation = Conversation()

        # Add system message if present in the async agent
        if self._async_agent._system_message:
            conversation.add_system_message(self._async_agent._system_message)

        # Add the message
        if isinstance(message, str):
            conversation.add_user_message(message)
        else:
            conversation.add_message(message)

        return conversation

    @classmethod
    def create_assistant(cls, name: str, **kwargs: Any) -> "MeepoAgent":
        """Create an assistant agent.

        Args:
            name: The name of the agent.
            **kwargs: Additional arguments to pass to create_assistant.

        Returns:
            A MeepoAgent wrapping an assistant AsyncMeepoAgent.
        """
        async_agent = AsyncMeepoAgent.create_assistant(name=name, **kwargs)
        return cls(async_agent)

    @classmethod
    def create_code_executor(cls, name: str, **kwargs: Any) -> "MeepoAgent":
        """Create a code executor agent.

        Args:
            name: The name of the agent.
            **kwargs: Additional arguments to pass to create_code_executor.

        Returns:
            A MeepoAgent wrapping a code executor AsyncMeepoAgent.
        """
        async_agent = AsyncMeepoAgent.create_code_executor(name=name, **kwargs)
        return cls(async_agent)

    @classmethod
    def create_user_proxy(cls, name: str, **kwargs: Any) -> "MeepoAgent":
        """Create a user proxy agent.

        Args:
            name: The name of the agent.
            **kwargs: Additional arguments to pass to create_user_proxy.

        Returns:
            A MeepoAgent wrapping a user proxy AsyncMeepoAgent.
        """
        async_agent = AsyncMeepoAgent.create_user_proxy(name=name, **kwargs)
        return cls(async_agent)

    @classmethod
    def from_agent(cls, agent: Any, name: str | None = None) -> "MeepoAgent":
        """Create a MeepoAgent from another agent.

        Args:
            agent: The agent to wrap.
            name: Optional name for the new agent.

        Returns:
            A MeepoAgent wrapping the provided agent.
        """
        async_agent = AsyncMeepoAgent.from_agent(agent, name)
        return cls(async_agent)
