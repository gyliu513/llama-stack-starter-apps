## Responses Basics

### Simple Response (`01_simple_response.py`)

Basic Responses API call using a single user prompt.

```bash
python -m examples.02_responses_basics.01_simple_response localhost 8321 --prompt "Hello"
```

### Tool Calling (`02_tool_calling.py`)

Call a simple function tool using the Responses API.

```bash
python -m examples.02_responses_basics.02_tool_calling localhost 8321 --prompt "Add 7 and 35."
```

### Conversation Turns (`03_conversation_turns.py`)

Multi-turn conversation using a shared conversation id.

```bash
python -m examples.02_responses_basics.03_conversation_turns localhost 8321
```
