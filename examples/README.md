# Llama Stack Examples

This folder contains a comprehensive collection of examples demonstrating how to build applications with Llama Stack. The examples are organized in a progressive learning path from fundamental concepts to complete applications.

## Setup Instructions

### Prerequisites

1. Set API keys for external services:
   ```bash
   # For web search capabilities
   # Get Tavily API keys from https://docs.tavily.com/documentation/quickstart
   export TAVILY_SEARCH_API_KEY=your_key_here
   ```

2. Start the Llama Stack server locally:
   ```bash
   conda create -n stack python=3.10
   conda activate stack
   pip install -U llama_stack

   # Start the server on localhost:8321
   llama stack run starter
   ```

3. Install required Python dependencies:
   ```bash
   cd <path-to-llama-stack-apps-repo>
   pip install -r requirements.txt
   ```

## Learning Path

We recommend following this learning path to build your understanding progressively:

### 1. 📚 Foundations (`01_foundations/`)

**What you'll learn:** Core building blocks of Llama Stack

Start here to understand the fundamental APIs and concepts:
- Client initialization and server health checks
- Chat completions with streaming
- System prompts and behavior control
- Vector databases and semantic search
- Document ingestion and retrieval
- Tool registration and MCP integration

**8 demos** covering everything from basic client setup to advanced tool integration.

[View detailed README](01_foundations/README.md)

**Example:**
```bash
python -m examples.01_foundations.01_client_setup localhost 8321
python -m examples.01_foundations.02_chat_completion localhost 8321 --prompt "Hello"
```

---

### 2. 💬 Responses Basics (`02_responses_basics/`)

**What you'll learn:** The Responses API for text generation

Build on foundations to master response generation:
- Simple text responses with instructions
- Tool calling through agents
- Multi-turn conversation management
- Real-time streaming responses
- Structured outputs with JSON schemas

**5 demos** demonstrating different response patterns.

[View detailed README](02_responses_basics/README.md)

**Example:**
```bash
python -m examples.02_responses_basics.01_simple_response localhost 8321 --prompt "Hello"
python -m examples.02_responses_basics.05_response_formats localhost 8321
```

---

### 3. 🔍 RAG - Retrieval-Augmented Generation (`03_rag/`)

**What you'll learn:** Building knowledge-grounded applications

Learn to ground model responses in retrieved documents:
- Basic RAG with file_search tool
- Multi-source retrieval from multiple vector stores
- Metadata-based filtering
- Chunking strategy optimization
- Hybrid search (local documents + web)

**5 demos** covering RAG techniques from simple to advanced.

[View detailed README](03_rag/README.md)

**Example:**
```bash
python -m examples.03_rag.01_simple_rag localhost 8321
python -m examples.03_rag.05_hybrid_search localhost 8321
```

---

### 4. 🤖 Agents (`04_agents/`)

**What you'll learn:** Building sophisticated conversational agents

Create intelligent agents with advanced capabilities:
- Simple chat agents with safety shields
- Multimodal agents (text + images)
- Document-grounded conversations
- Custom tool integration
- RAG-enabled agents
- ReACT (Reasoning and Acting) patterns
- Multi-agent systems and routing

**7 demos** showcasing different agent architectures.

[View detailed README](04_agents/README.md)

**Example:**
```bash
python -m examples.04_agents.01_simple_agent_chat --host localhost --port 8321
python -m examples.04_agents.07_agent_routing --host localhost --port 8321
```

---

## Complete Applications

After completing the learning path, explore these full-featured applications:

### 🏪 Agent Store (`agent_store/`)

**Interactive chat application with Gradio UI**

A complete web-based chat interface for interacting with agents. Features include:
- Web-based UI built with Gradio
- Session management
- Tool integration
- Customizable agent configurations

[View detailed README](agent_store/README.md)

**Run:**
```bash
python -m examples.agent_store.app localhost 8321
```

---

### 🎨 Interior Design Assistant (`interior_design_assistant/`)

**Specialized multimodal assistant**

An example of a domain-specific assistant that combines:
- Vision capabilities for image understanding
- Text generation for descriptions
- Custom tools for specialized tasks

[View detailed README](interior_design_assistant/README.md)

**Run:**
```bash
python -m examples.interior_design_assistant.app
```

---

## Supporting Resources

### `client_tools/`
Reusable tool implementations that can be used across examples:
- Calculator tool
- Web search tool (Tavily/Brave)
- Stock ticker data tool

### `shared/`
Shared utility functions and helpers:
- Model selection and validation
- Context building utilities
- Common helper functions

### `resources/`
Sample data, documents, and assets used in examples

## Quick Reference

### Common Commands

```bash
# Foundations
python -m examples.01_foundations.02_chat_completion localhost 8321 --prompt "Your question"
python -m examples.01_foundations.04_vector_db_basics localhost 8321

# Responses
python -m examples.02_responses_basics.02_tool_calling localhost 8321
python -m examples.02_responses_basics.04_streaming_responses localhost 8321

# RAG
python -m examples.03_rag.01_simple_rag localhost 8321
python -m examples.03_rag.04_chunking_strategies localhost 8321

# Agents
python -m examples.04_agents.01_simple_agent_chat --host localhost --port 8321
python -m examples.04_agents.05_rag_agent --host localhost --port 8321

# Applications
python -m examples.agent_store.app localhost 8321
python -m examples.interior_design_assistant.app
```

### Common Parameters

Most examples accept these parameters:
- `--host`: Server hostname (default: localhost)
- `--port`: Server port (default: 8321)
- `--model_id`: Specific model to use (optional)
- `--prompt`: User prompt for single-turn examples

## Troubleshooting

**Server not running:**
```bash
llama stack run starter
```

**Missing API keys:**
```bash
export TAVILY_SEARCH_API_KEY=your_key_here
```

**Dependencies not installed:**
```bash
pip install -r requirements.txt
```

## Next Steps

1. Start with `01_foundations` to learn the basics
2. Progress through `02_responses_basics` and `03_rag`
3. Master agent development with `04_agents`
4. Explore complete applications (`agent_store`, `interior_design_assistant`)
5. Build your own application using these patterns!

## Additional Resources

- [Llama Stack Documentation](https://llama-stack.readthedocs.io/)
- [Llama Stack GitHub](https://github.com/meta-llama/llama-stack)
- [Discord Community](https://discord.gg/llama-stack)
- [Client SDKs](https://github.com/meta-llama/llama-stack-client-python)
