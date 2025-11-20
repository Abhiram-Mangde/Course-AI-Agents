*How to make agents stateful, aware, and capable of long-term reasoning.*

# What is Context Engineering?

**Context Engineering** is the practice of carefully designing:

- Prompts & system instructions
- Conversation/session state
- Memory
- Knowledge retrieval
- Constraints, rules & tools
- Long-term reasoning strategies
- Information compression

The goal is to create **predictable, reliable, and intelligent agent behaviors**.

## Why Context Engineering Matters

LLMs aren’t magical.
They behave based on whatever **context** you feed them.

Poor context → inconsistent answers
Great context → stable, high-quality agent reasoning

Agents must maintain:
- user goals
- steps performed
- external data retrieved
- tool outputs
- constraints

*Without context engineering, even advanced agents behave like chatbots.*

---
## Types of Memory (Technical Breakdown)

Agents need memory systems to:
- store facts
- retain previous actions
- remember steps across loops
- avoid repeating work
- refer to history
- combine data from tools

There are **4 major types of memory:**

### 1. Short-Term Memory (Session Memory)
- Lives only inside the current conversation or agent loop
- Stored in the messages list
- Lost when session resets

*Example:*
```python
session_history = [
  {"role": "user", "content": "Find me top 5 AI companies"},
  {"role": "assistant", "content": "Here they are..."}
]
```

*Used for:*
- chatbots
- multi-turn reasoning
- tracking instructions

### 2. Long-Term Memory (Vector Memory)

*Stored permanently in:*
- FAISS
- Pinecone
- Chroma DB
- Weaviate
- Milvus

Stores **embeddings** → lets agent remember knowledge.

*Used for:*
- personal assistants
- enterprise knowledge
- long projects
- multi-session tasks

### 3. Scratchpad / Working Memory (Hidden to user)

The LLM maintains internal reasoning such as:
- Plan
- Thought processes
- Subtasks
- Tool selection criteria

You **never store this** — the LLM uses it internally.

### 4. Persistent Memory (Storage-Based)

Files or databases that persist across runs.

*Examples:*
- user profiles
- preferences
- task state
- logs

previous results

*Used for:*
- long-term assistants
- multi-agent systems
- product-grade agents

---

## Building a Stateful Agent

Below is a minimal **stateful agent** structure:
```python
class ChatSession:
    def __init__(self):
        self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
    
    def get(self):
        return self.history
```

*Example usage:*
```python
session = ChatSession()

session.add("user", "Hello agent")
session.add("assistant", "Hi, how can I help you?")
session.add("user", "Remember that my favorite color is blue")
```

*This stores memory inside the session.*

---

## Adding LLM Reasoning With Session Memory
```python 
from openai import OpenAI
client = OpenAI()

def agent_response(session, message):
    session.add("user", message)

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=session.get()
    ).choices[0].message.content

    session.add("assistant", response)
    return response
```

**Run:**
```python 
agent_response(session, "What's my favorite color?")
```
--- 

## Implementing Long-Term Memory (Vector DB)

Now let’s extend the agent with vector memory.

**Step 1 — Setup Vector DB (FAISS)**
```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384
index = faiss.IndexFlatL2(dimension)
stored_texts = []
```

**Step 2 — Store Memory**
```python
def store_memory(text):
    emb = model.encode([text])
    index.add(emb)
    stored_texts.append(text)
```

**Step 3 — Recall Memory**
```python
def recall(query, k=3):
    emb = model.encode([query])
    distances, indices = index.search(emb, k)

    results = []
    for idx in indices[0]:
        if idx < len(stored_texts):
            results.append(stored_texts[idx])
    return results
```

**Step 4 — Agent Uses Both Session + Vector Memory**
```python
def agent_with_memory(session, message):
    # store message in long-term memory
    store_memory(message)

    retrieved = recall(message)

    session_prompt = [
        {"role": "system", "content": "You are a memory-augmented agent."},
        {"role": "system", "content": f"Relevant past memory: {retrieved}"}
    ] + session.get() + [{"role": "user", "content": message}]
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=session_prompt
    ).choices[0].message.content
    
    session.add("assistant", response)
    return response
```
---

## Context Compression

When conversations become long, context must be summarized so the agent stays efficient.

**Compression Example**
```python
def compress_history(history):
    summary = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize the following conversation:"},
            {"role": "user", "content": str(history)}
        ]
    ).choices[0].message.content
    return summary
```

You can replace full history with compressed context after 20–30 messages.

---

## Designing Context Templates
*Good agent context includes:*

1. System role
2. Goal
3. Constraints
4. Tools
5. Memory retrieved
6. Current user query
7. Past conversation

Example template:
```yaml
You are an autonomous agent.
Goal: Solve the user task safely and efficiently.
Follow these rules:
- Use tools when helpful.
- Keep reasoning concise.
- Think step-by-step.
Memory relevant to the task:
{{retrieved_memory}}

Conversation summary:
{{compressed_history}}

Current task:
{{user_query}}
```

*This template dramatically improves reliability.*

---

## Full Stateful Agent

Below is a more complete example of an agent with:
- session memory
- vector memory
- context engineering
- dynamic prompts

[Code](https://github.com/Abhiram-Mangde/Course-AI-Agents/blob/main/Day-3/Python%20Scripts/FullStateAgent.py)