# llama-stack-apps

[![Discord](https://img.shields.io/discord/1257833999603335178)](https://discord.gg/llama-stack)

This repo shows examples of applications built on top of [Llama Stack](https://github.com/meta-llama/llama-stack). Starting with Llama 3.1, you can build agentic applications capable of:

- Breaking down tasks and performing multi-step reasoning
- Using tools to perform actions:
  - Built-in: the model has built-in knowledge of tools like search or code interpreter
  - Zero-shot: the model can learn to call tools using previously unseen, in-context tool definitions
- Providing system-level safety protections using models like Llama Guard

An agentic app requires a few components:
- Ability to run inference on the underlying Llama series of models
- Ability to run safety checks using the Llama Guard series of models
- Ability to execute tools, including a code execution environment, and loop using the model's multi-step reasoning process

All of these components are now offered by a single Llama Stack Distribution. The [Llama Stack](https://github.com/meta-llama/llama-stack) defines and standardizes these components and many others that are needed to make building Generative AI applications smoother.

## Getting Started with Llama Stack Apps

To get started with Llama Stack Apps, you'll need to:

1. Install prerequisites
2. Start a Llama Stack server
3. Run example applications

### 1. Install Prerequisites

**Python Packages**

We recommend creating an isolated conda Python environment.

```bash
# Create and activate a virtual environment
conda create -n stack python=3.12
conda activate stack
cd <path-to-llama-stack-apps-repo>

# Install dependencies
pip install -r requirements.txt
```

This will install all dependencies required to (1) build and start a Llama Stack server and (2) connect your client app to the Llama Stack server.

### 2. Start a Llama Stack Server

Install Llama Stack and start the server:

```bash
pip install -U llama_stack

# Start the server on localhost:8321
llama stack run starter
```

Once your server is started, you should see output:
```
...
Listening on :::8321
INFO:     Started server process [587053]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://[::]:8321 (Press CTRL+C to quit)
```

For more advanced setups, see the [Llama Stack Getting Started Guide](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html).

### 3. Set API Keys (Optional)

Some examples require API keys for external services:

```bash
# For web search capabilities
# Get Tavily API keys from https://docs.tavily.com/documentation/quickstart
export TAVILY_SEARCH_API_KEY=your_key_here
```

## Learning Path: Examples

This repository provides a structured learning path through progressive examples. Start with the foundations and work your way up to building complete applications.

### 📚 [01_foundations](examples/01_foundations)
**Learn the core building blocks of Llama Stack**

- Client setup and connection management
- Chat completions with streaming support
- System prompts and behavior customization
- Vector databases and semantic search
- Document insertion and retrieval
- Tool registration and MCP integration

**Quick Start:**
```bash
python -m examples.01_foundations.01_client_setup localhost 8321
python -m examples.01_foundations.02_chat_completion localhost 8321 --prompt "Hello"
```

### 💬 [02_responses_basics](examples/02_responses_basics)
**Master the Responses API for text generation**

- Simple response generation
- Tool calling with agents
- Multi-turn conversations
- Streaming responses
- Structured outputs with JSON schemas

**Quick Start:**
```bash
python -m examples.02_responses_basics.01_simple_response localhost 8321 --prompt "Hello"
```

### 🔍 [03_rag](examples/03_rag)
**Build Retrieval-Augmented Generation systems**

- Simple RAG with file_search
- Multi-source RAG across vector stores
- Metadata filtering and targeted retrieval
- Chunking strategies optimization
- Hybrid search (local + web)

**Quick Start:**
```bash
python -m examples.03_rag.01_simple_rag localhost 8321
```

### 🤖 [04_agents](examples/04_agents)
**Create sophisticated conversational agents**

- Simple agent chat with safety shields
- Multimodal agents (text + images)
- Document-grounded conversations
- Custom tool integration
- RAG-enabled agents
- ReACT (Reasoning and Acting) patterns
- Multi-agent coordination and routing

**Quick Start:**
```bash
python -m examples.04_agents.01_simple_agent_chat --host localhost --port 8321
```

### 🏪 [agent_store](examples/agent_store)
**Interactive chat application with UI**

A full-featured chat interface built with Gradio for interacting with agents.

**Quick Start:**
```bash
python -m examples.agent_store.app localhost 8321
```

<img src="demo.png" alt="Chat App" width="600"/>

### 🎨 [interior_design_assistant](examples/interior_design_assistant)
**Multimodal assistant application**

An example of a specialized assistant that combines vision and text capabilities.

**Quick Start:**
```bash
python -m examples.interior_design_assistant.app
```

## Example Projects Structure

```
examples/
├── 01_foundations/        # Core APIs and concepts
├── 02_responses_basics/   # Response generation patterns
├── 03_rag/               # Retrieval-Augmented Generation
├── 04_agents/            # Agent development
├── agent_store/          # Chat UI application
├── interior_design_assistant/  # Specialized multimodal app
├── client_tools/         # Reusable tool implementations
├── shared/               # Shared utilities
└── resources/            # Sample data and assets
```

## The Llama Stack Client SDK

Check out our client SDKs for connecting to Llama Stack server in multiple programming languages:
- [Python](https://github.com/meta-llama/llama-stack-client-python)
- [Node.js](https://github.com/meta-llama/llama-stack-client-node)

## Using VirtualEnv Instead of Conda

> [!NOTE]
> While you can run the apps using `venv`, installation of a distribution requires conda.

#### Linux

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # For Command Prompt
# or
.\venv\Scripts\Activate.ps1  # For PowerShell
# or
source venv/Scripts/activate  # For Git Bash
```

The instructions thereafter (including `pip install -r requirements.txt`) remain the same.

## Additional Resources

- [Llama Stack Documentation](https://llamastack.github.io/)
- [Llama Stack GitHub](https://github.com/llamastack/llama-stack)
- [Discord Community](https://discord.gg/llama-stack)

## Contributing

We welcome contributions! Please see our contributing guidelines and feel free to submit issues or pull requests.

## License

See the [LICENSE](LICENSE) file for details.
