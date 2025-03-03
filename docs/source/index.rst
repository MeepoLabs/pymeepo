Welcome to pymeepo's documentation!
===================================

.. image:: https://img.shields.io/pypi/v/pymeepo.svg
   :target: https://pypi.org/project/pymeepo/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pymeepo.svg
   :target: https://pypi.org/project/pymeepo/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/meepolabs/pymeepo.svg
   :target: https://github.com/meepolabs/pymeepo/blob/main/LICENSE
   :alt: License

.. image:: https://readthedocs.org/projects/pymeepo/badge/?version=latest
   :target: https://pymeepo.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

A universal Python SDK for integrating and building AI agents across different frameworks (LangChain, AutoGen, etc.) and providers.

Overview
--------

pymeepo is a Python SDK that provides a unified interface for working with AI agents from various frameworks. It enables developers to:

- **Framework Integration**: Seamlessly integrate agents from LangChain, AutoGen, and other frameworks
- **Provider Abstraction**: Work with multiple LLM providers through a consistent interface
- **Framework Interoperability**: Enable communication between agents built with different frameworks
- **Developer Experience**: Intuitive APIs with strong type hints and documentation

Key Features
------------

Universal Framework Support
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Native support for popular agent frameworks (LangChain, AutoGen)
- Framework-agnostic base interfaces
- Adapter system for easy framework integration
- Common protocol definitions

Provider Integration
~~~~~~~~~~~~~~~~~~~~

- Direct provider connections (OpenAI, Anthropic)
- LiteLLM integration for broad provider support
- Provider-agnostic message formats
- Cost optimization utilities

Framework Interoperability
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Cross-framework message passing
- Unified memory interfaces
- Standardized tool protocols
- Common type system

Development Tools
~~~~~~~~~~~~~~~~~

- Framework adapters and utilities
- Testing and mocking tools
- Debugging helpers
- Performance monitoring

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   core_concepts
   getting_started

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
