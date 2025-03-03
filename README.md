# pymeepo

[![PyPI version](https://img.shields.io/pypi/v/pymeepo.svg)](https://pypi.org/project/pymeepo/)
[![Python versions](https://img.shields.io/pypi/pyversions/pymeepo.svg)](https://pypi.org/project/pymeepo/)
[![License](https://img.shields.io/github/license/meepolabs/pymeepo.svg)](https://github.com/meepolabs/pymeepo/blob/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/pymeepo/badge/?version=latest)](https://pymeepo.readthedocs.io/en/latest/?badge=latest)

A universal Python SDK for integrating and building AI agents across different frameworks (LangChain, AutoGen, etc.) and providers.

## Overview

pymeepo is a Python SDK that provides a unified interface for working with AI agents from various frameworks. It enables developers to:

- **Framework Integration**: Seamlessly integrate agents from LangChain, AutoGen, and other frameworks
- **Provider Abstraction**: Work with multiple LLM providers through a consistent interface
- **Framework Interoperability**: Enable communication between agents built with different frameworks
- **Developer Experience**: Intuitive APIs with strong type hints and documentation

## Key Features

- **Universal Framework Support**
  - Native support for popular agent frameworks (LangChain, AutoGen)
  - Framework-agnostic base interfaces
  - Adapter system for easy framework integration
  - Common protocol definitions

- **Provider Integration**
  - Direct provider connections (OpenAI, Anthropic)
  - LiteLLM integration for broad provider support
  - Provider-agnostic message formats
  - Cost optimization utilities

- **Framework Interoperability**
  - Cross-framework message passing
  - Unified memory interfaces
  - Standardized tool protocols
  - Common type system

- **Development Tools**
  - Framework adapters and utilities
  - Testing and mocking tools
  - Debugging helpers
  - Performance monitoring

## Installation

```bash
pip install pymeepo
```

Or with Poetry:

```bash
poetry add pymeepo
```

## Quick Example

```python
from pymeepo import Agent, LangChainAdapter, AutoGenAdapter

# Create agents from different frameworks
langchain_agent = LangChainAdapter.from_agent(
    "your-langchain-agent",
    provider="openai",
    api_key="your-api-key"
)

autogen_agent = AutoGenAdapter.from_agent(
    "your-autogen-agent",
    provider="anthropic",
    api_key="your-api-key"
)

# They can now work together seamlessly
result = await langchain_agent.run(
    "Process this data",
    tools=[autogen_agent.as_tool()]
)
```

## Documentation

For detailed documentation, visit [pymeepo.readthedocs.io](https://pymeepo.readthedocs.io).

The documentation includes:
- Getting Started Guide
- Framework Integration Guide
- Provider Configuration
- API Reference
- Examples and Tutorials

## Contributing

We welcome contributions! Please check out our [contributing guidelines](CONTRIBUTING.md) for details on:
- Setting up your development environment
- Adding new framework adapters
- Running tests
- Submitting pull requests

## License

This project is licensed under the [GNU General Public License v3.0 (GPLv3)](LICENSE).
