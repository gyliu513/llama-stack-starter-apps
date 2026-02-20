# 02 - Responses Basics: Student Learning Guide

> 📚 **Module 02: Responses API** This module teaches you the higher-level Responses API, which provides enhanced capabilities beyond basic chat completions including tool calling, conversation management, and structured outputs.

---

## 🎯 Module Overview

In Module 01, you learned about the **Chat Completions API** - the foundation for talking to AI models. Now you'll learn about the **Responses API**, which is a more powerful abstraction that adds:

- 🛠️ **Tool Calling**: Let AI use functions and external tools
- 💬 **Conversation Management**: Maintain context across multiple turns
- 📊 **Structured Outputs**: Get JSON responses that match your schema
- ⚡ **Streaming**: Real-time response generation
- 🎨 **Response Formatting**: Control output structure

Think of it this way:
- **Chat Completions API**: Basic phone call
- **Responses API**: Video conference with screen sharing, file transfer, and recording

---

## 📖 Core Concepts Deep Dive

### Concept 1: Responses API vs Chat Completions API

**What's the Difference?**

```mermaid
graph TB
    subgraph "Chat Completions API (Module 01)"
        A1[Your Prompt] --> B1[Language Model]
        B1 --> C1[Text Response]
    end

    subgraph "Responses API (Module 02)"
        A2[Your Prompt] --> B2[Agent Layer]
        B2 --> C2{Needs Tool?}
        C2 -->|Yes| D2[Call Tool]
        C2 -->|No| E2[Generate Text]
        D2 --> F2[Tool Result]
        F2 --> B2
        E2 --> G2[Formatted Response]
    end

    style A1 fill:#e1f5ff
    style A2 fill:#e1f5ff
    style B2 fill:#fff3cd
    style G2 fill:#d4edda
```

**Comparison Table**:

| Feature | Chat Completions API | Responses API |
|---------|---------------------|---------------|
| **Purpose** | Direct model interface | Enhanced agent interface |
| **Tool Calling** | Manual implementation | Built-in support |
| **Conversations** | Manual state management | Automatic conversation IDs |
| **Structured Output** | Text parsing required | Native JSON schema support |
| **Use Case** | Simple Q&A, text generation | Complex workflows, tool use |
| **Configuration** | `messages` parameter | `instructions` + `input` |

**When to Use Each**:

| Scenario | Use This |
|----------|----------|
| Simple question answering | Chat Completions |
| Need to call external APIs/tools | Responses API |
| Multi-turn conversations with memory | Responses API |
| Want structured JSON output | Responses API |
| Batch text processing | Chat Completions |
| Building agent workflows | Responses API |

---

### Concept 2: Instructions Parameter

In the Responses API, the **instructions** parameter is similar to the system prompt in Chat Completions, but more powerful.

**Structure**:
```python
# Chat Completions (Module 01)
messages = [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello"}
]

# Responses API (Module 02)
instructions = "You are helpful. Use tools when needed."
input = [{"role": "user", "content": "Hello"}]
```

**Instructions vs System Prompt**:

```mermaid
graph LR
    A[Instructions] --> B[Behavior Guidelines]
    A --> C[Tool Usage Guidance]
    A --> D[Output Format Rules]
    A --> E[Conversation Strategy]

    F[System Prompt] --> G[Behavior Guidelines]
    F --> H[Personality]

    style A fill:#d4edda
    style F fill:#e1f5ff
```

**Example Instructions**:

1. **Basic Helper**:
```
You are a helpful assistant that provides clear, accurate answers.
```

2. **Tool-Using Agent**:
```
You are a research assistant. When asked about current events, use web search.
When asked about documents, use file search. Cite your sources.
```

3. **Structured Response Agent**:
```
You analyze customer feedback and categorize it. Always respond in JSON format
with fields: sentiment (positive/negative/neutral), category, and priority.
```

---

### Concept 3: Tool Calling

**What is Tool Calling?**

Tool calling allows the AI to use external functions to accomplish tasks it cannot do through text generation alone.

**Tools AI Can Use**:
- 🌐 **Web Search**: Get current information from the internet
- 📁 **File Search**: Query vector databases for document retrieval
- 🧮 **Calculator**: Perform precise mathematical computations
- 📊 **Data Fetching**: Get stock prices, weather, etc.
- 🔧 **Custom Functions**: Anything you define!

**Tool Calling Flow**:
```mermaid
sequenceDiagram
    participant User
    participant Agent as Responses API
    participant Model as Language Model
    participant Tool as External Tool

    User->>Agent: "What's the weather in Tokyo?"

    Agent->>Model: Process request
    Model->>Model: Analyze: Need current data

    Note over Model: Decides to call weather tool

    Model-->>Agent: Tool Call Request:<br/>get_weather city="Tokyo"

    Agent->>Tool: Execute get_weather("Tokyo")
    Tool->>Tool: Fetch from API
    Tool-->>Agent: Result: 22°C, Sunny

    Agent->>Model: Here's the tool result
    Model->>Model: Generate natural response

    Model-->>Agent: "The weather in Tokyo is<br/>22°C and sunny."

    Agent-->>User: Display response
```

**Tool Definition Format**:
```python
{
    "type": "web_search",  # Built-in tool type
    # Or for custom tools:
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {
        "city": {"type": "string", "description": "City name"}
    }
}
```

**Tool Choice Options**:

| Option | Behavior |
|--------|----------|
| `auto` | Model decides whether to use tools |
| `required` | Model must use at least one tool |
| `none` | Model cannot use tools |
| `{"type": "web_search"}` | Model must use this specific tool |

---

### Concept 4: Conversation Management

**The Problem**: How do we maintain context across multiple messages?

**Traditional Approach (Manual)**:
```python
# You have to track history yourself
conversation_history = []
conversation_history.append({"role": "user", "content": "My name is Alice"})
# ... get response ...
conversation_history.append({"role": "assistant", "content": "Hi Alice!"})
conversation_history.append({"role": "user", "content": "What's my name?"})
# Send entire history every time!
```

**Responses API Approach (Automatic)**:
```python
# Create conversation once
conversation_id = "conv-123"

# Just send new messages
# The server remembers everything!
response = client.responses.create(
    input=[{"role": "user", "content": "My name is Alice"}],
    conversation_id=conversation_id
)

# Later...
response = client.responses.create(
    input=[{"role": "user", "content": "What's my name?"}],
    conversation_id=conversation_id  # Same ID!
)
# Response: "Your name is Alice!"
```

**Conversation Flow**:
```mermaid
flowchart TD
    A[User: 'My name is Alice'] --> B{Conversation ID exists?}
    B -->|No| C[Create new conversation<br/>ID: conv-123]
    B -->|Yes| D[Load conversation history]

    C --> E[Store in conversation:<br/>User: My name is Alice]
    D --> E

    E --> F[Generate response:<br/>Assistant: Hi Alice!]

    F --> G[Add to conversation history]

    G --> H[User: What's my name?]

    H --> I[Load full history:<br/>1. User: My name is Alice<br/>2. Assistant: Hi Alice!<br/>3. User: What's my name?]

    I --> J[Generate response with context:<br/>Assistant: Your name is Alice!]

    style C fill:#fff3cd
    style I fill:#d4edda
    style J fill:#e1f5ff
```

**Benefits**:
- ✅ Automatic context preservation
- ✅ Server-side storage (no client state)
- ✅ Simplified code
- ✅ Better for long conversations

---

### Concept 5: Streaming Responses

Streaming in the Responses API works similarly to Chat Completions, but with additional event types.

**Event Types in Streaming**:

| Event Type | Description |
|------------|-------------|
| `content` | Text token from the model |
| `tool_call` | Model wants to call a tool |
| `tool_result` | Result from tool execution |
| `done` | Response completed |

**Streaming Flow**:
```mermaid
sequenceDiagram
    participant User
    participant App
    participant API as Responses API

    User->>App: Submit query with stream=True

    App->>API: Create streaming response

    loop For each event
        API-->>App: Event chunk
        alt Content Event
            App->>App: Print text token
        else Tool Call Event
            App->>App: Show "Using tool X"
        else Tool Result Event
            App->>App: Show "Got result"
        end
    end

    API-->>App: Done event

    App-->>User: Complete response displayed
```

**Code Pattern**:
```python
response = client.responses.create(
    model=model_id,
    instructions=instructions,
    input=[{"role": "user", "content": prompt}],
    stream=True  # Enable streaming
)

for event in response:
    if event.type == "content":
        print(event.content, end="", flush=True)
    elif event.type == "tool_call":
        print(f"\n[Using {event.tool_name}...]")
```

---

### Concept 6: Structured Outputs (JSON Mode)

One of the most powerful features of the Responses API is guaranteed JSON output.

**Two Modes**:

1. **JSON Object Mode**: Valid JSON, but no schema enforcement
2. **JSON Schema Mode**: JSON that matches your exact schema

**JSON Object Mode**:
```mermaid
flowchart LR
    A[User Prompt] --> B[Model with<br/>response_format:<br/>json_object]
    B --> C{Valid JSON?}
    C -->|Yes| D[Return Response]
    C -->|No| E[Retry/Validate]
    E --> B

    style B fill:#fff3cd
    style D fill:#d4edda
```

**JSON Schema Mode**:
```mermaid
flowchart LR
    A[User Prompt] --> B[Your Schema Definition]
    B --> C[Model with<br/>response_format:<br/>json_schema]
    C --> D{Matches<br/>Schema?}
    D -->|Yes| E[Return Response]
    D -->|No| F[Regenerate]
    F --> C

    style B fill:#e1f5ff
    style C fill:#fff3cd
    style E fill:#d4edda
```

**Example Schema**:
```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "age"]
}
```

**Why This Matters**:
- ✅ No parsing errors
- ✅ Type safety guaranteed
- ✅ Direct integration with your app
- ✅ Reliable data extraction

---

## 📝 Demo Walkthroughs

### Demo 1: Simple Response

**Learning Goal**: Understand basic Responses API usage and how it differs from Chat Completions.

**Code Flow**:
```mermaid
flowchart TD
    A[START] --> B[Initialize Client]
    B --> C[Select/Verify Model]
    C --> D[Define Instructions<br/>'You are a helpful assistant']
    D --> E[Format Input Messages<br/>role: user, content: prompt]
    E --> F[Call responses.create]
    F --> G{Success?}
    G -->|Yes| H[Extract output_text]
    G -->|No| I[❌ Error Handling]
    H --> J[Print Response]
    J --> K[END]

    style D fill:#fff3cd
    style E fill:#e1f5ff
    style J fill:#d4edda
```

**Key Differences from Chat Completions**:

| Aspect | Chat Completions | Responses API |
|--------|-----------------|---------------|
| **API Endpoint** | `client.chat.completions.create()` | `client.responses.create()` |
| **Behavior Config** | `messages[0]` with system role | `instructions` parameter |
| **Input Format** | `messages` (list) | `input` (list) |
| **Response Field** | `choices[0].message.content` | `output_text` or `output` |

**Try This**:
```bash
# Basic response
python -m demos.02_responses_basics.01_simple_response localhost 8321 \
  --prompt "Explain what APIs are in simple terms"

# Custom instructions
python -m demos.02_responses_basics.01_simple_response localhost 8321 \
  --instructions "You explain things using food analogies" \
  --prompt "What is a database?"
```

---

### Demo 2: Tool Calling

**Learning Goal**: Enable AI to use external tools like web search.

**Complete Tool Calling Flow**:
```mermaid
sequenceDiagram
    participant User
    participant App
    participant API as Responses API
    participant Model
    participant Tool as Web Search

    User->>App: "Who was the 42nd president?"

    App->>API: Create response with<br/>tools=[web_search]

    API->>Model: Process request

    Note over Model: Analyzes: Need current/factual data<br/>Decides: Use web_search

    Model-->>API: Tool Call: web_search<br/>query="42nd president US"

    API->>Tool: Execute search
    Tool->>Tool: Query search engine
    Tool-->>API: Results: William J. Clinton...

    API->>Model: Here's what search found

    Model->>Model: Generate answer using results

    Model-->>API: "The 42nd president was<br/>William J. Clinton (1993-2001)"

    API-->>App: Final response

    App-->>User: Display answer
```

**Tool Configuration**:
```python
# Make web search available
tools = [{"type": "web_search"}]

# Force the model to use it
tool_choice = {"type": "web_search"}

response = client.responses.create(
    model=model_id,
    instructions="Search the web and provide factual answers",
    input=[{"role": "user", "content": "Who was the 42nd president?"}],
    tools=tools,
    tool_choice=tool_choice
)
```

**When to Use Tool Calling**:

| Scenario | Reason |
|----------|--------|
| Current events | Model training data is outdated |
| Factual lookup | Need verified information |
| Calculations | Want precise math results |
| Data retrieval | Need to fetch from databases/APIs |
| File search | Querying document collections |

**Try This**:
```bash
# Requires TAVILY_SEARCH_API_KEY in environment
python -m demos.02_responses_basics.02_tool_calling localhost 8321 \
  --prompt "Search for the current population of Tokyo"
```

**What to Observe**:
- The model decides to use web search
- Search query is generated
- Results are integrated into the response
- Answer is current and factual

---

### Demo 3: Conversation Turns

**Learning Goal**: Maintain context across multiple conversation turns.

**Multi-Turn Conversation Architecture**:
```mermaid
flowchart TD
    A[START Conversation] --> B[Generate Conversation ID<br/>e.g., 'conv-12345']

    subgraph "Turn 1"
        C1[User: 'My favorite color is blue'] --> D1[Create Response<br/>with conversation_id]
        D1 --> E1[Store in conversation:<br/>User msg + Assistant reply]
    end

    B --> C1

    subgraph "Turn 2"
        C2[User: 'What's my favorite color?'] --> D2[Create Response<br/>SAME conversation_id]
        D2 --> E2[Load conversation history]
        E2 --> F2[Context includes Turn 1!]
        F2 --> G2[Response: 'Your favorite color is blue']
    end

    E1 --> C2

    subgraph "Turn 3"
        C3[User: 'Why do I like that color?'] --> D3[Create Response<br/>SAME conversation_id]
        D3 --> E3[Load full history:<br/>Turns 1 & 2]
        E3 --> F3['That color' = blue]
        F3 --> G3[Response refers to blue]
    end

    G2 --> C3

    style B fill:#fff3cd
    style E2 fill:#d4edda
    style E3 fill:#d4edda
    style F3 fill:#e1f5ff
```

**Conversation Memory**:
```
┌─────────────────────────────────────────┐
│ Conversation ID: conv-12345             │
├─────────────────────────────────────────┤
│ Turn 1:                                 │
│   User: "My favorite color is blue"     │
│   Assistant: "Blue is a lovely color!"  │
├─────────────────────────────────────────┤
│ Turn 2:                                 │
│   User: "What's my favorite color?"     │
│   Assistant: "Your favorite color       │
│              is blue."                  │
├─────────────────────────────────────────┤
│ Turn 3:                                 │
│   User: "Why do I like it?"             │
│   [Context: "it" = blue from Turn 1]    │
│   Assistant: "Blue is often associated  │
│              with calmness..."          │
└─────────────────────────────────────────┘
```

**Code Pattern**:
```python
import uuid

# Generate unique conversation ID
conversation_id = str(uuid.uuid4())

# Turn 1
response1 = client.responses.create(
    model=model_id,
    instructions="You are helpful",
    input=[{"role": "user", "content": "My name is Alice"}],
    conversation_id=conversation_id  # Remember this!
)

# Turn 2 - Context is preserved!
response2 = client.responses.create(
    model=model_id,
    instructions="You are helpful",
    input=[{"role": "user", "content": "What's my name?"}],
    conversation_id=conversation_id  # Same ID!
)
# Response will be: "Your name is Alice!"
```

**Try This**:
```bash
python -m demos.02_responses_basics.03_conversation_turns localhost 8321

# The demo has multiple turns pre-programmed:
# 1. User introduces themselves
# 2. User asks model to remember something
# 3. User asks if model remembers
```

**Experiment**:
Modify the demo to add more turns and test the limits of conversation memory!

---

### Demo 4: Streaming Responses

**Learning Goal**: Stream responses in real-time across conversation turns.

**Streaming + Conversation Flow**:
```mermaid
sequenceDiagram
    participant User
    participant App
    participant API as Responses API

    Note over User,API: Turn 1 (with streaming)

    User->>App: "Tell me about AI"
    App->>API: create(stream=True, conversation_id=conv1)

    loop Stream events
        API-->>App: content: "Artificial"
        App-->>User: Display "Artificial"
        API-->>App: content: " Intelligence"
        App-->>User: Display " Intelligence"
        API-->>App: content: " is..."
        App-->>User: Display " is..."
    end

    API-->>App: done event

    Note over User,API: Turn 2 (same conversation)

    User->>App: "Give me an example"
    App->>API: create(stream=True, conversation_id=conv1)

    Note over API: Loads Turn 1 context

    loop Stream events
        API-->>App: content tokens...
        App-->>User: Display tokens...
    end
```

**Event Types You'll See**:
```python
for event in response_stream:
    if event.type == "content":
        # Text generation
        print(event.content, end="", flush=True)

    elif event.type == "tool_call":
        # Model is calling a tool
        print(f"\n[Using {event.tool_name}...]")

    elif event.type == "tool_result":
        # Tool finished
        print(f"\n[Got result from {event.tool_name}]")

    elif event.type == "done":
        # Response complete
        print("\n[Response complete]")
```

**Streaming Benefits**:

| Without Streaming | With Streaming |
|-------------------|----------------|
| Wait 5-10 seconds | See progress immediately |
| "Is it working?" | "It's typing!" |
| Poor UX for long responses | Smooth, progressive display |
| Can't cancel mid-response | Can stop if needed |

**Try This**:
```bash
python -m demos.02_responses_basics.04_streaming_responses localhost 8321

# Watch the response appear token-by-token!
```

---

### Demo 5: Response Formats (JSON Mode)

**Learning Goal**: Generate structured JSON outputs with schema validation.

**JSON Object Mode vs JSON Schema Mode**:

```mermaid
graph TB
    subgraph "json_object Mode"
        A1[User: 'Analyze sentiment:<br/>This product is amazing!'] --> B1[Model]
        B1 --> C1{Valid JSON?}
        C1 -->|Yes| D1["output_text:<br/>{sentiment: 'positive'}"]
        C1 -->|No| E1[Retry]
        E1 --> B1
    end

    subgraph "json_schema Mode"
        A2[User: 'Analyze sentiment'] --> B2[Schema Required!<br/>properties: sentiment, score]
        B2 --> C2[Model]
        C2 --> D2{Matches<br/>Schema?}
        D2 -->|Yes| E2["output_text:<br/>{sentiment: 'positive',<br/>score: 0.95}"]
        D2 -->|No| F2[Regenerate]
        F2 --> C2
    end

    style D1 fill:#fff3cd
    style E2 fill:#d4edda
```

**Schema Definition Example**:
```python
# Define exact structure you want
schema = {
    "type": "object",
    "properties": {
        "sentiment": {
            "type": "string",
            "enum": ["positive", "negative", "neutral"]
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
        },
        "keywords": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["sentiment", "confidence"]
}

# Use it
response = client.responses.create(
    model=model_id,
    instructions="Analyze the sentiment of reviews",
    input=[{"role": "user", "content": "This product is amazing!"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "sentiment_analysis",
            "schema": schema
        }
    }
)

# Response is GUARANTEED to match schema!
result = json.loads(response.output_text)
print(result["sentiment"])  # Always valid!
```

**Use Cases**:

| Scenario | Format | Why |
|----------|--------|-----|
| Data extraction | json_schema | Need specific fields |
| Sentiment analysis | json_schema | Consistent structure |
| Classification | json_schema | Enum values |
| Form filling | json_schema | Type validation |
| General JSON | json_object | No schema needed |

**Try This**:
```bash
python -m demos.02_responses_basics.05_response_formats localhost 8321
```

**What You'll See**:
1. **JSON Object Mode**: Valid JSON but flexible structure
2. **JSON Schema Mode**: Strictly matches the defined schema

**Experiment**:
Modify the schema to:
- Add new required fields
- Change data types
- Add array properties
- Define enum constraints

---

## 🎓 Learning Checkpoints

### Checkpoint 1: API Understanding
- [ ] Can you explain the difference between Chat Completions API and Responses API?
- [ ] When would you choose one over the other?
- [ ] What is the `instructions` parameter used for?

### Checkpoint 2: Tool Calling
- [ ] What kinds of tasks require tool calling?
- [ ] How does the model decide to use a tool?
- [ ] What's the difference between `tool_choice: auto` and `tool_choice: required`?

### Checkpoint 3: Conversations
- [ ] How does conversation_id help maintain context?
- [ ] What happens if you use a different conversation_id?
- [ ] Can you reuse a conversation_id after a long time?

### Checkpoint 4: JSON Modes
- [ ] What's the difference between json_object and json_schema?
- [ ] When would you need schema validation?
- [ ] What happens if the model can't match your schema?

---

## 💡 Practice Exercises

### Exercise 1: Multi-Tool Agent
Build an agent that can use multiple tools.

**Challenge**:
```python
tools = [
    {"type": "web_search"},
    {"type": "calculator"},
    # Add file_search if you have documents
]

# Create queries that need different tools:
# 1. "What's 15% of 250?" → calculator
# 2. "Who won the latest Nobel Prize?" → web_search
# 3. Multiple tools: "Search for the GDP of Japan and calculate
#    what 25% of that would be"
```

---

### Exercise 2: Conversation Bot
Create a chatbot that remembers user preferences.

**Requirements**:
- Ask user for their name (Turn 1)
- Ask for favorite topic (Turn 2)
- Ask a question using both pieces of info (Turn 3)
- Verify memory: "What's my name?" (Turn 4)

**Hint**: Use a single conversation_id throughout!

---

### Exercise 3: Structured Data Extractor
Build a schema to extract information from unstructured text.

**Example Task**: Parse product reviews
```python
schema = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "rating": {"type": "integer", "minimum": 1, "maximum": 5},
        "pros": {"type": "array", "items": {"type": "string"}},
        "cons": {"type": "array", "items": {"type": "string"}},
        "recommended": {"type": "boolean"}
    },
    "required": ["product_name", "rating", "recommended"]
}
```

Test with various review texts!

---

## 🔄 Comparison Summary

### Chat Completions vs Responses API

```mermaid
graph TB
    A[Your Task] --> B{Task Type?}

    B -->|Simple Q&A| C[Use Chat Completions]
    B -->|Need Tools| D[Use Responses API]
    B -->|Multi-turn conversation| D
    B -->|Structured output| D
    B -->|Batch processing| C

    C --> E[Lower level<br/>More control<br/>Simpler]
    D --> F[Higher level<br/>More features<br/>More powerful]

    style C fill:#e1f5ff
    style D fill:#d4edda
```

---

## 🐛 Common Issues & Solutions

### Issue: Tool not being called
**Symptoms**: Model generates text instead of using tool

**Solutions**:
```python
# Force tool use:
tool_choice = {"type": "web_search"}  # Specific tool
# or
tool_choice = "required"  # Any tool must be used

# Make instructions clearer:
instructions = "You MUST use web_search for current information"
```

---

### Issue: Conversation context lost
**Symptoms**: Model doesn't remember previous turns

**Solutions**:
- Verify you're using the SAME conversation_id
- Check conversation_id is a string
- Ensure server hasn't been restarted (conversations are in-memory)

---

### Issue: JSON schema validation fails
**Symptoms**: Errors about schema mismatch

**Solutions**:
- Verify schema syntax (valid JSON Schema format)
- Check required fields are not too restrictive
- Simplify schema if model struggles with complex structures
- Add more context in instructions about expected format

---

## 📚 Additional Resources

- **JSON Schema Documentation**: [json-schema.org](https://json-schema.org)
- **Tool Calling Best Practices**: See Module 04 (Agents) for advanced patterns
- **Conversation Design**: Study chatbot UX principles

---

## 🎯 Next Module Preview

**Module 03: RAG (Retrieval-Augmented Generation)**

Now that you understand:
- ✅ Vector search (Module 01)
- ✅ Tool calling (Module 02)

You're ready to combine them into **RAG systems** that:
- Search document collections
- Retrieve relevant context
- Generate grounded responses
- Cite sources

**Module 04: Agents**

Build complete autonomous agents that:
- Use multiple tools
- Maintain long conversations
- Handle complex multi-step tasks
- Process multimodal inputs (text + images)

---

## ✅ Module Completion Checklist

- [ ] Used the Responses API for basic text generation
- [ ] Implemented tool calling with web search
- [ ] Created multi-turn conversations with conversation_id
- [ ] Streamed responses in real-time
- [ ] Generated JSON output with schema validation

**Congratulations on completing Responses Basics!** 🎉

You now understand the higher-level Responses API and can build agents that use tools, maintain conversations, and generate structured outputs.

**Ready for more?** → Proceed to **Module 03: RAG**
