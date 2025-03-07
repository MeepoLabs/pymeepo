"""Adapters for various AI agent frameworks.

This package provides adapters for different AI agent frameworks, allowing them
to work seamlessly with the Meepo platform. Each framework has its own
subpackage with specific implementations.

Available adapters:
- autogen: Adapter for AutoGen framework
- langchain: Adapter for LangChain framework (coming soon)
"""

from typing import TypeAlias, Union

from autogen_agentchat.agents import BaseChatAgent

from pymeepo.adapters.autogen import AutogenAdapter
from pymeepo.core.base_agent import BaseMeepoAgent

# Update this type alias as we add support for more frameworks
# SupportedAgent = Union[BaseChatAgent, LangChainAgent, CustomAgent, ...]
SupportedAgents: TypeAlias = Union[BaseChatAgent]  # noqa: UP007


def adapt(agent: SupportedAgents) -> BaseMeepoAgent[SupportedAgents]:
    """Adapt any supported agent to work with the Meepo platform.

    This function automatically detects the type of agent and returns the
    appropriate adapter. If the agent type is not supported, it raises a
    ValueError.

    Example:
        ```python
        from autogen import AssistantAgent
        from pymeepo.adapters import adapt

        # Create an AutoGen agent
        autogen_agent = AssistantAgent(name="assistant")

        # Adapt it to work with Meepo - detects it's an AutoGen agent
        agent = adapt(autogen_agent)

        # Use the adapted agent
        result = await agent.run("What is the Meepo platform?")
        ```

    Args:
        agent: The agent to adapt. Must be an instance of a supported
            framework's agent class.

    Returns:
        A Meepo agent that wraps the provided agent.

    Raises:
        ValueError: If the agent type is not supported.
    """
    # Check for AutoGen agent
    if isinstance(agent, BaseChatAgent):
        return AutogenAdapter(agent)

    # Add more framework checks here as we add support
    # Example:
    # if isinstance(agent, LangchainAgent):
    #     return LangchainAdapter(agent)

    raise ValueError(
        f"Unsupported agent type: {type(agent).__name__}. "
        "Currently supported frameworks: AutoGen"
    )


__all__ = ["adapt", "AutogenAdapter", "SupportedAgents"]
