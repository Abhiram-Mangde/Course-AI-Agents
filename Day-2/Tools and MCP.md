*How agents extend their capabilities by connecting to external systems.*

# What Are Tools?

A Tool is any actionable capability that extends what an LLM-based agent can do.

Without tools → an agent is limited to text reasoning.
With tools → an agent can **interact with the real world**.

*Tools allow agents to:*

- Query APIs (weather, stock price, flight search…)
- Read/write data (files, databases, vector DBs…)
- Perform calculations
- Trigger workflows (send emails, automate tasks…)
- Launch long-running operations (reports, scripts, pipelines…)

*Why Tools Matter*

> **Because LLMs are not databases, not calculators, and not deterministic.
Tools solve that.**

**How Agents Use Tools**

Agents use their reasoning to determine:
1. Do I need a tool?
2. Which tool is appropriate?
3. Which parameters should I pass?

*This transforms the LLM from a chatbot into a fully capable system.*

---

## Tool Design Principles (Technical)
**1. Deterministic**

- The same input → the same output
- This helps reduce hallucinations and makes agents safer.

**2. Idempotent**

Running the same tool multiple times should NOT break anything.
(Important because agents may retry actions.)

**3. Clear Schemas**

Tools must define:
- name
- description
- input schema
- output structure

*LLMs rely heavily on schema clarity to choose the right tool.*

**4. Safe Defaults**

Example:
- default pagination
- default file limit
- safe fallback values

**5. Strict Input Validation**
- Never trust LLM input directly.
- Validate:
    - types
    - structure
    - missing fields
    - ranges

**6. Short Execution Time**

Tools should:
- run fast
- avoid blocking
- use async if long-running

Long tasks should use **MCP long-running operations.**

---

## Tool Example
**A simple OpenAI-style function tool.**
```python
tools = [
  {
    "type": "function",
    "function": {
      "name": "search_weather",
      "description": "Get weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {"type": "string"}
        },
        "required": ["city"]
      }
    }
  }
]
```

## How the Agent Uses This Tool

**Step 1 — LLM detects need for weather data**
```
“TOOL CALL: search_weather({city: 'London'})”
```
**Step 2 — Controller executes tool**

```python
def search_weather(city):
    # in reality this would call an API
    return {"temp": 22, "condition": "sunny"}
```

**Step 3 — LLM receives tool results and continues reasoning**

[Full working Code]()

---
## What Is MCP (Model Context Protocol)?

MCP is a **standard protocol** that allows LLM-based agents to interact with tools, resources, and external services in a structured way.

Think of MCP as:

> **The USB for AI tools**

A universal way to connect agents to tools.

## What MCP Provides:

| MCP Feature                | Why It Matters                        |
| -------------------------- | ------------------------------------- |
| Standard tool schemas      | Agents know exactly how to call tools |
| Long-running operations    | Agents can perform heavy tasks        |
| Resources                  | Agents can read/write documents       |
| Prompts                    | Shared templates across clients       |
| Authentication             | Secure tool usage                     |
| Multi-client compatibility | Same tool works for many agents       |
---

## Core Concept: Servers & Clients

### MCP Server
Hosts tools, prompts, resources.
Examples:
- weather API
- filesystem
- database queries
- automation scripts

### MCP Client
The AI agent (or application) that connects to the server.
---

## MCP Architecture (Technical)
*The full flow:*

1. Agent uses reasoning to decide it needs a tool.
2. MCP Client builds a standardized request:
```
{"method": "callTool", "params": {...}}
```

3. MCP Server validates schema & executes the tool.
4. Server returns:
```
{"result": {...}, "events": [...]}
```
5. Agent uses the result to continue reasoning.
---

## MCP Built-In Features
**Tool Schemas**

Machines (LLMs) can reason about:
- what a tool does
- required parameters
- valid types

**Streaming Responses**
- Useful for logs, progress bars, or streaming data.

**Long-Running Operations**

Some tasks take minutes or hours:
- report generation
- crawling websites
- indexing large files

MCP supports async streaming:
```
start → progress → progress → done
```

**Authentication**
- API keys
- OAuth
- JWT
- secure headers

**Standardized Communication**
Everything uses JSON-RPC over:
- WebSockets
- stdin/stdout
- HTTP

---

## Practical MCP Example

**Directory Structure**
```
mcp_server/
  └── tools.json
```

**tools.json**
```json
{
  "tools": [
    {
      "name": "lookup_stock",
      "description": "Fetch stock price",
      "inputSchema": {
        "type": "object",
        "properties": {
          "symbol": { "type": "string" }
        },
        "required": ["symbol"]
      }
    }
  ]
}
```

## How an Agent Calls This Tool
*Agent asks:*
```
“TOOL: lookup_stock({symbol: 'stockName'})”
```

**MCP Server executes:**
```python
def lookup_stock(symbol):
    # In real life, this might call yahoo finance
    return {"symbol": symbol, "price": 1000}
```

**Server returns the response to agent.**

Agent continues reasoning:
```
“The current price of stock is Rs.1000.”
```

[Complete Code for MCP Server]()

---