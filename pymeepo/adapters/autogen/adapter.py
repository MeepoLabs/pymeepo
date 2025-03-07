"""AutoGen adapter implementation."""

from collections.abc import AsyncGenerator, Mapping, Sequence
from typing import Any, cast

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import ChatMessage
from autogen_core import CancellationToken

from pymeepo.core.base_agent import BaseMeepoAgent


class AutogenAdapter(BaseMeepoAgent[BaseChatAgent]):
    """Adapter for AutoGen agents.

    This adapter wraps an existing AutoGen agent and delegates all operations
    to it, making it compatible with the Meepo platform.

    Example:
        ```python
        from autogen import AssistantAgent
        from pymeepo.adapters.autogen import AutogenAdapter

        # Create an AutoGen agent
        autogen_agent = AssistantAgent(name="assistant")

        # Adapt it to work with Meepo
        agent = AutogenAdapter(autogen_agent)

        # Use the adapted agent
        result = await agent.run("What is the Meepo platform?")
        ```
    """

    _internal_agent: BaseChatAgent

    def __init__(self, agent: BaseChatAgent) -> None:
        """Initialize the adapter.

        Args:
            agent: The AutoGen agent to adapt
        """
        super().__init__(name=agent.name, description=agent.description)
        self._internal_agent = agent

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        """Get the types of messages this agent can produce.

        Returns:
            A sequence of ChatMessage types that this agent can produce
        """
        # cast to return type to satisfy the type checker
        return cast(
            Sequence[type[ChatMessage]],
            self._internal_agent.produced_message_types,
        )

    async def on_messages(
        self,
        messages: Sequence[ChatMessage],
        cancellation_token: CancellationToken,
    ) -> Response:
        """Process incoming messages and generate a response.

        Args:
            messages: The messages to process
            cancellation_token: Token for cancellation

        Returns:
            The agent's response
        """
        return await self._internal_agent.on_messages(
            messages, cancellation_token
        )

    async def on_messages_stream(
        self,
        messages: Sequence[ChatMessage],
        cancellation_token: CancellationToken,
    ) -> AsyncGenerator[Any, None]:
        """Process messages and generate a streaming response.

        Args:
            messages: The messages to process
            cancellation_token: Token for cancellation

        Returns:
            An async generator producing the response
        """
        async for chunk in self._internal_agent.on_messages_stream(
            messages, cancellation_token
        ):
            yield chunk

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        """Reset the agent's state.

        Args:
            cancellation_token: Token for cancellation
        """
        await self._internal_agent.on_reset(cancellation_token)

    async def save_state(self) -> Mapping[str, Any]:
        """Save the agent's state.

        Returns:
            A mapping containing the agent's state
        """
        # cast to return type to satisfy the type checker
        return cast(Mapping[str, Any], await self._internal_agent.save_state())

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the agent's state.

        Args:
            state: A mapping containing the agent's state
        """
        await self._internal_agent.load_state(state)

    async def close(self) -> None:
        """Release any resources held by the agent."""
        await self._internal_agent.close()
