## Available Examples

### Client Setup (`01_client_setup.py`)

Validate your client connection by performing a health check.

```bash
python -m examples.01_foundations.01_client_setup localhost 8321
```

### Chat Completion (`02_chat_completion.py`)

Basic inference with chat completions using the Llama Stack client.

```bash
python -m examples.01_foundations.02_chat_completion localhost 8321 --prompt "Hello"

# Stream tokens as they arrive
python -m examples.01_foundations.02_chat_completion localhost 8321 --prompt "Hello" --stream
```

### System Prompts (`03_system_prompts.py`)

Customize the system prompt for a single-turn chat.

```bash
python -m examples.01_foundations.03_system_prompts localhost 8321 --prompt "Hello"

# Override the system prompt
python -m examples.01_foundations.03_system_prompts localhost 8321 --system_prompt "You are concise." --prompt "Hello"
```

### Vector DB Basics (`04_vector_db_basics.py`)

Register a vector store, add a document, and run a search.

```bash
python -m examples.01_foundations.04_vector_db_basics localhost 8321

# Provide custom text and query
python -m examples.01_foundations.04_vector_db_basics localhost 8321 --text "Llama Stack unifies AI services." --query "What does Llama Stack do?"
```

### Insert Documents (`05_insert_documents.py`)

Create (or reuse) a vector store and insert documents from URLs or a local directory.

```bash
python -m examples.01_foundations.05_insert_documents localhost 8321

# Insert files from a local directory
python -m examples.01_foundations.05_insert_documents localhost 8321 --file_dir ./docs

# Insert into an existing vector store
python -m examples.01_foundations.05_insert_documents localhost 8321 --vector_store_id <vector-store-id>
```

### Search Vectors (`06_search_vectors.py`)

Insert documents into a vector store and run a vector search.

```bash
python -m examples.01_foundations.06_search_vectors localhost 8321 --query "What does Llama Stack do?"
```
 
### Tool Registration (`07_tool_registration.py`)

Register custom tools (calculator, ticker data, web search) for an agent.

```bash
export TAVILY_SEARCH_API_KEY=...
python -m examples.01_foundations.07_tool_registration localhost 8321
```

### MCP Tools (`08_mcp_tools.py`)

Start a local MCP server and register its tools with Llama Stack.

```bash
# Terminal 1: start the MCP server (requires: pip install mcp)
python -m examples.01_foundations.08_mcp_tools serve

# Terminal 2: register the MCP toolgroup with Llama Stack
llama-stack-client toolgroups register plus-tools \
  --provider-id model-context-protocol \
  --mcp-endpoint "http://localhost:8000/sse"

# Terminal 2: invoke the add tool through the runtime
python -m examples.01_foundations.08_mcp_tools run localhost 8321 --mcp_endpoint http://localhost:8000/sse --tool_name add --a 1 --b 1
```
