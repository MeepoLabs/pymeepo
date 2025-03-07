"""Base class for all Meepo agents."""

from abc import ABC

from autogen_agentchat.agents import BaseChatAgent


class BaseMeepoAgent(BaseChatAgent, ABC):
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
    """
