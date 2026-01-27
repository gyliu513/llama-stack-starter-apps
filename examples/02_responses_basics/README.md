## Responses Basics

### Simple Response (`01_simple_response.py`)

Basic Responses API call using a single user prompt.

```bash
python -m examples.02_responses_basics.01_simple_response localhost 8321 --prompt "Hello"
```

### Tool Calling (`02_tool_calling.py`)

Tool calling via an agent (calculator, ticker data, web search).

```bash
python -m examples.02_responses_basics.02_tool_calling localhost 8321 --prompt "Search the web for who was the 42nd president of the United States and answer with the name only."
```

### Conversation Turns (`03_conversation_turns.py`)

Multi-turn conversation using a shared conversation id.

```bash
python -m examples.02_responses_basics.03_conversation_turns localhost 8321
```

### Streaming Responses (`04_streaming_responses.py`)

Stream agent tool calls and outputs.

```bash
python -m examples.02_responses_basics.04_streaming_responses localhost 8321
```

### Response Formats (`05_response_formats.py`)

Structured outputs with JSON mode and JSON schema.

```bash
python -m examples.02_responses_basics.05_response_formats localhost 8321
```
