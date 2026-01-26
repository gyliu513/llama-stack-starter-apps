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
