"""Base class for all Meepo agents."""

from abc import ABC
from typing import Any, Generic, TypeVar

from autogen_agentchat.agents import BaseChatAgent

T = TypeVar("T")


class BaseMeepoAgent(BaseChatAgent, Generic[T], ABC):
    """Abstract base class for all Meepo agents.

    This class serves as a wrapper around AutoGen's BaseChatAgent, providing
    a foundation for implementing agents from various frameworks in the Meepo
    platform. Framework-specific implementations (like AutoGen, LangChain,
    etc.) will be provided by MeepoLabs, along with additional methods for
    platform integration.

    Required Methods (must be implemented by subclasses):
    - on_messages(messages, cancellation_token) -> Response
        Process incoming messages and generate a response.
    - on_reset(cancellation_token) -> None
        Reset the agent to its initialization state.
    - produced_message_types -> Sequence[type[ChatMessage]]
        The types of messages that the agent can produce.

    Optional Methods (have default implementations):
    - on_messages_stream(messages, cancellation_token) -> AsyncGenerator
        Streaming version of on_messages. Default calls on_messages.
    - save_state() -> Mapping[str, Any]
        Export agent state. Default returns empty dict.
    - load_state(state) -> None
        Restore agent from saved state. Default is no-op.
    - close() -> None
        Release resources. Default is no-op.
    - run(task, cancellation_token) -> TaskResult
        Run a task. Default implementation handles various task types.
    - run_stream(task, cancellation_token) -> AsyncGenerator
        Streaming version of run. Default handles various task types.

    Framework-specific implementations will:
    1. Inherit from this class
    2. Implement the required methods
    3. Override optional methods if needed
    4. Add framework-specific functionality
    5. Provide Meepo platform integration methods

    The Meepo platform will provide concrete implementations for various
    frameworks, ensuring consistent behavior and seamless integration across
    different AI agent frameworks.

    Args:
        T: The type of the internal agent being wrapped. Must be a subclass
           of BaseChatAgent.
    """

    _internal_agent: T

    def __getattr__(self, name: str) -> Any:
        """Delegate any unknown attributes to the internal agent.

        This method provides automatic delegation of attributes to the internal
        agent, allowing framework-specific implementations to expose all their
        native functionality through the Meepo adapter.

        Args:
            name: The name of the attribute to get

        Returns:
            The attribute from the internal agent

        Raises:
            AttributeError: If the attribute doesn't exist or no internal agent
        """
        if self._internal_agent is None:
            raise AttributeError(
                f"{self.__class__.__name__} has no internal agent"
            )
        if hasattr(self._internal_agent, name):
            return getattr(self._internal_agent, name)
        raise AttributeError(
            f"{self.__class__.__name__} has no attribute '{name}'"
        )
